// Local Files Base URL (for localhost server)
const BASE_URL = 'problem-xmls/';

// URL 매개변수에서 config 파일명 가져오기
function getConfigFileName() {
    const urlParams = new URLSearchParams(window.location.search);
    const configParam = urlParams.get('config');
    return configParam ? `${configParam}.xml` : 'config.xml';
}

// 1. 데이터 로딩 함수들
function loadConfig() {
    console.log('🔄 Config 로딩 시작...');
    return new Promise((resolve, reject) => {
        try {
            const configFileName = getConfigFileName();
            const configUrl = BASE_URL + configFileName;
            console.log(`📥 ${configFileName} XMLHttpRequest 시도...`, configUrl);
            const xhr = new XMLHttpRequest();
            xhr.open('GET', configUrl, true);
            
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    console.log('📡 XMLHttpRequest 상태:', xhr.status, xhr.statusText);
                    
                    if (xhr.status === 200 || xhr.status === 0) { // 0은 로컬 파일
                        try {
                            console.log('📄 XML 텍스트 읽기...');
                            const xmlText = xhr.responseText;
                            console.log('📄 XML 내용 길이:', xmlText.length);
                            console.log('📄 XML 내용 미리보기:', xmlText.substring(0, 200));
                            
                            console.log('🔍 XML 파싱 시작...');
                            const parser = new DOMParser();
                            const xmlDoc = parser.parseFromString(xmlText, 'text/xml');
                            
                            // XML 파싱 에러 체크
                            const parseError = xmlDoc.querySelector('parsererror');
                            if (parseError) {
                                console.error('❌ XML 파싱 에러:', parseError.textContent);
                                reject(new Error('XML 파싱 오류: ' + parseError.textContent));
                                return;
                            }
                            
                            console.log('✅ XML 파싱 성공');
                            
                            // XML을 JSON 형태로 변환
                            console.log('🔄 데이터 추출 시작...');
                            const titleElement = xmlDoc.querySelector('title');
                            console.log('📝 Title 요소:', titleElement);
                            const title = titleElement ? titleElement.textContent : 'No Title';
                            console.log('📝 추출된 Title:', title);
                            
                            // 설정 정보 추출
                            const settingsElement = xmlDoc.querySelector('settings');
                            const showSolutions = settingsElement ? 
                                settingsElement.querySelector('showSolutions')?.textContent === 'true' : true;
                            console.log('⚙️ 해설 표시 설정:', showSolutions);
                            
                            const sectionElements = xmlDoc.querySelectorAll('section');
                            console.log('📂 Section 요소들:', sectionElements.length, '개');
                            
                            const sections = Array.from(sectionElements).map((section, index) => {
                                const sectionData = {
                                    title: section.getAttribute('title'),
                                    file: section.getAttribute('file'),
                                    count: parseInt(section.getAttribute('count'))
                                };
                                console.log(`📂 Section ${index + 1}:`, sectionData);
                                return sectionData;
                            });
                            
                            // Concatenate 요소들 처리
                            const concatenateElements = xmlDoc.querySelectorAll('concatenate');
                            console.log('🔗 Concatenate 요소들:', concatenateElements.length, '개');
                            
                            const concatenates = Array.from(concatenateElements).map((concat, index) => {
                                const sources = Array.from(concat.querySelectorAll('source')).map(source => ({
                                    file: source.getAttribute('file')
                                }));
                                const concatenateData = {
                                    title: concat.getAttribute('title'),
                                    count: parseInt(concat.getAttribute('count')),
                                    sources: sources
                                };
                                console.log(`🔗 Concatenate ${index + 1}:`, concatenateData);
                                return concatenateData;
                            });
                            
                            // 모든 섹션을 순서대로 수집 (sections 컨테이너 내의 모든 자식 노드)
                            console.log('📋 통합 섹션 순서 수집 시작...');
                            const allSections = [];
                            const sectionsContainer = xmlDoc.querySelector('sections');
                            
                            if (sectionsContainer) {
                                const sectionNodes = sectionsContainer.children;
                                
                                for (let i = 0; i < sectionNodes.length; i++) {
                                    const node = sectionNodes[i];
                                    console.log(`📋 노드 ${i + 1}: ${node.tagName}`);
                                    
                                    if (node.tagName === 'section') {
                                        allSections.push({
                                            type: 'section',
                                            title: node.getAttribute('title'),
                                            file: node.getAttribute('file'),
                                            count: parseInt(node.getAttribute('count'))
                                        });
                                    } else if (node.tagName === 'concatenate') {
                                        const sources = Array.from(node.querySelectorAll('source')).map(source => ({
                                            file: source.getAttribute('file')
                                        }));
                                        allSections.push({
                                            type: 'concatenate',
                                            title: node.getAttribute('title'),
                                            count: parseInt(node.getAttribute('count')),
                                            sources: sources
                                        });
                                    }
                                }
                            }
                            
                            // sections 바깥에 있는 concatenate들도 추가 (하위 호환성)
                            const rootConcatenates = xmlDoc.querySelectorAll('exercise > concatenate');
                            rootConcatenates.forEach(concat => {
                                const sources = Array.from(concat.querySelectorAll('source')).map(source => ({
                                    file: source.getAttribute('file')
                                }));
                                allSections.push({
                                    type: 'concatenate',
                                    title: concat.getAttribute('title'),
                                    count: parseInt(concat.getAttribute('count')),
                                    sources: sources
                                });
                            });
                            
                            console.log('📋 통합 섹션 순서:', allSections.map((s, i) => `${i+1}. ${s.type}: ${s.title}`));
                            
                            const result = { title, sections, concatenates, allSections, showSolutions };
                            console.log('✅ Config 로딩 완료:', result);
                            resolve(result);
                        } catch (parseError) {
                            console.error('❌ XML 처리 오류:', parseError);
                            reject(parseError);
                        }
                    } else {
                        const error = new Error(`Config 파일 로딩 실패: ${xhr.status}`);
                        console.error('❌ XMLHttpRequest 실패:', error);
                        reject(error);
                    }
                }
            };
            
            xhr.onerror = function() {
                const error = new Error('XMLHttpRequest 네트워크 오류');
                console.error('❌ XMLHttpRequest 네트워크 오류:', error);
                reject(error);
            };
            
            xhr.send();
        } catch (error) {
            console.error('❌ Config 로딩 오류:', error);
            reject(error);
        }
    });
}

function loadProblems(filename) {
    console.log(`🔄 문제 파일 로딩 시작: ${filename}`);
    return new Promise((resolve, reject) => {
        try {
            const problemUrl = BASE_URL + filename;
            console.log(`📥 ${filename} XMLHttpRequest 시도...`, problemUrl);
            const xhr = new XMLHttpRequest();
            xhr.open('GET', problemUrl, true);
            
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    console.log(`📡 XMLHttpRequest 상태 (${filename}):`, xhr.status, xhr.statusText);
                    
                    if (xhr.status === 200 || xhr.status === 0) { // 0은 로컬 파일
                        try {
                            console.log(`📄 XML 텍스트 읽기 (${filename})...`);
                            const xmlText = xhr.responseText;
                            console.log(`📄 XML 내용 길이 (${filename}):`, xmlText.length);
                            
                            console.log(`🔍 XML 파싱 시작 (${filename})...`);
                            const parser = new DOMParser();
                            const xmlDoc = parser.parseFromString(xmlText, 'text/xml');
                            
                            // XML 파싱 에러 체크
                            const parseError = xmlDoc.querySelector('parsererror');
                            if (parseError) {
                                console.error(`❌ XML 파싱 에러 (${filename}):`, parseError.textContent);
                                reject(new Error('XML 파싱 오류: ' + parseError.textContent));
                                return;
                            }
                            
                            console.log(`✅ XML 파싱 성공 (${filename})`);
                            
                            // XML에서 문제들을 추출하여 배열로 변환
                            console.log(`🔄 문제 데이터 추출 시작 (${filename})...`);
                            const problemElements = xmlDoc.querySelectorAll('problem');
                            console.log(`🧩 문제 개수 (${filename}):`, problemElements.length);
                            
                            const problems = Array.from(problemElements).map((problem, index) => {
                                console.log(`🔍 문제 ${index + 1} 처리 중...`);
                                const problemData = {
                                    description: problem.querySelector('description')?.textContent || '',
                                    code: problem.querySelector('code')?.textContent || null,
                                    input: problem.querySelector('input')?.textContent || null,
                                    output: problem.querySelector('output')?.textContent || null,
                                    hint: problem.querySelector('hint')?.textContent || null,
                                    solution: problem.querySelector('solution')?.textContent || null
                                };
                                console.log(`🧩 문제 ${index + 1} 데이터:`, {
                                    description: problemData.description.substring(0, 50) + '...',
                                    hasCode: !!problemData.code,
                                    hasInput: !!problemData.input,
                                    hasOutput: !!problemData.output,
                                    hasHint: !!problemData.hint,
                                    hasSolution: !!problemData.solution
                                });
                                return problemData;
                            });
                            
                            console.log(`✅ 문제 파일 로딩 완료 (${filename}):`, problems.length, '개');
                            resolve(problems);
                        } catch (parseError) {
                            console.error(`❌ XML 처리 오류 (${filename}):`, parseError);
                            reject(parseError);
                        }
                    } else {
                        const error = new Error(`문제 파일 로딩 실패: ${filename} (${xhr.status})`);
                        console.error(`❌ XMLHttpRequest 실패 (${filename}):`, error);
                        reject(error);
                    }
                }
            };
            
            xhr.onerror = function() {
                const error = new Error(`XMLHttpRequest 네트워크 오류: ${filename}`);
                console.error(`❌ XMLHttpRequest 네트워크 오류 (${filename}):`, error);
                reject(error);
            };
            
            xhr.send();
        } catch (error) {
            console.error(`❌ 문제 파일 로딩 오류 (${filename}):`, error);
            reject(error);
        }
    });
}

// 2. 문제 처리 함수들
function shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

function selectRandomProblems(problems, count) {
    if (problems.length <= count) {
        return problems;
    }
    return shuffleArray(problems).slice(0, count);
}

// 3. HTML 렌더링 함수들
function renderProblem(problem, number, showSolutions = true) {
    let html = `<div class="problem">`;
    html += `<div class="problem-header"><span class="problem-number">${number}. </span>${problem.description}</div>`;
    
    if (problem.code) {
        html += `<div class="code-block">${problem.code}</div>`;
    }
    
    if (problem.input) {
        html += `<div class="input-example">${problem.input}</div>`;
    }
    
    if (problem.output) {
        html += `<div class="output-example">${problem.output}</div>`;
    }
    
    if (problem.hint) {
        html += `<div class="hint">${problem.hint}</div>`;
    }
    
    if (problem.solution && showSolutions) {
        html += `<div class="solution">${problem.solution}</div>`;
    }
    
    html += `</div>`;
    return html;
}

function renderSection(title, problems, startNumber, showSolutions = true) {
    let html = `<h2>${title}</h2>`;
    problems.forEach((problem, index) => {
        html += renderProblem(problem, startNumber + index, showSolutions);
    });
    return html;
}

function renderDocument(config, allProblems) {
    const titleElement = document.getElementById('main-title');
    const contentElement = document.getElementById('content');
    
    titleElement.textContent = config.title;
    
    let html = '';
    let problemNumber = 1;
    
    // 통합 섹션 순서대로 렌더링 (우선순위)
    if (config.allSections && config.allSections.length > 0) {
        console.log('📋 통합 섹션 순서대로 렌더링 시작...');
        config.allSections.forEach((section, index) => {
            console.log(`📋 ${index + 1}번째 섹션 처리: ${section.type} - ${section.title}`);
            
            if (section.type === 'section') {
                // Section 렌더링
                const sectionProblems = allProblems[section.file] || [];
                const selectedProblems = selectRandomProblems(sectionProblems, section.count);
                
                html += renderSection(section.title, selectedProblems, problemNumber, config.showSolutions);
                problemNumber += selectedProblems.length;
                
            } else if (section.type === 'concatenate') {
                // Concatenate 렌더링
                console.log(`🔗 Concatenate 섹션 처리: ${section.title}`);
                
                // 여러 소스 파일의 문제들을 하나로 병합
                let mergedProblems = [];
                section.sources.forEach(source => {
                    const sourceProblems = allProblems[source.file] || [];
                    console.log(`📁 ${source.file}에서 ${sourceProblems.length}개 문제 추가`);
                    mergedProblems = mergedProblems.concat(sourceProblems);
                });
                
                console.log(`🔗 총 ${mergedProblems.length}개 문제에서 ${section.count}개 선택`);
                const selectedProblems = selectRandomProblems(mergedProblems, section.count);
                
                html += renderSection(section.title, selectedProblems, problemNumber, config.showSolutions);
                problemNumber += selectedProblems.length;
            }
        });
    } else {
        // 하위 호환성: 기존 방식 사용
        console.log('📋 기존 방식으로 렌더링 (하위 호환성)');
        
        // Section 렌더링
        config.sections.forEach(section => {
            const sectionProblems = allProblems[section.file] || [];
            const selectedProblems = selectRandomProblems(sectionProblems, section.count);
            
            html += renderSection(section.title, selectedProblems, problemNumber, config.showSolutions);
            problemNumber += selectedProblems.length;
        });
        
        // Concatenate 렌더링
        if (config.concatenates) {
            config.concatenates.forEach(concat => {
                console.log(`🔗 Concatenate 섹션 처리: ${concat.title}`);
                
                // 여러 소스 파일의 문제들을 하나로 병합
                let mergedProblems = [];
                concat.sources.forEach(source => {
                    const sourceProblems = allProblems[source.file] || [];
                    console.log(`📁 ${source.file}에서 ${sourceProblems.length}개 문제 추가`);
                    mergedProblems = mergedProblems.concat(sourceProblems);
                });
                
                console.log(`🔗 총 ${mergedProblems.length}개 문제에서 ${concat.count}개 선택`);
                const selectedProblems = selectRandomProblems(mergedProblems, concat.count);
                
                html += renderSection(concat.title, selectedProblems, problemNumber, config.showSolutions);
                problemNumber += selectedProblems.length;
            });
        }
    }
    
    contentElement.innerHTML = html;
}

// 4. 메인 실행 함수
async function init() {
    console.log('🚀 애플리케이션 초기화 시작...');
    try {
        console.log('⚙️ Config 로딩 중...');
        const config = await loadConfig();
        console.log('✅ Config 로딩 성공:', config);
        
        const allProblems = {};
        
        console.log('📚 문제 파일들 로딩 시작...');
        
        // 모든 필요한 파일 목록 수집
        const allFiles = new Set();
        
        // Section 파일들 추가
        config.sections.forEach(section => {
            allFiles.add(section.file);
        });
        
        // Concatenate 파일들 추가
        if (config.concatenates) {
            config.concatenates.forEach(concat => {
                concat.sources.forEach(source => {
                    allFiles.add(source.file);
                });
            });
        }
        
        // 모든 문제 파일 병렬 로딩
        const loadPromises = Array.from(allFiles).map(async file => {
            console.log(`📖 로딩 중: ${file}`);
            allProblems[file] = await loadProblems(file);
            console.log(`✅ 완료: ${file}`);
        });
        
        await Promise.all(loadPromises);
        console.log('✅ 모든 문제 파일 로딩 완료:', Object.keys(allProblems));
        
        // 문서 렌더링
        console.log('🎨 문서 렌더링 시작...');
        renderDocument(config, allProblems);
        console.log('🎉 애플리케이션 초기화 완료!');
        
    } catch (error) {
        console.error('❌ 초기화 오류:', error);
        console.error('❌ 오류 스택:', error.stack);
        document.getElementById('main-title').textContent = '오류 발생';
        document.getElementById('content').innerHTML = 
            `<div style="color: red; padding: 20px; border: 1px solid red;">
                <h3>파일 로딩 오류</h3>
                <p><strong>오류 메시지:</strong> ${error.message}</p>
                <p><strong>가능한 원인:</strong></p>
                <ul>
                    <li>브라우저에서 파일을 직접 열었을 때 CORS 정책으로 인한 차단</li>
                    <li>XML 파일이 존재하지 않거나 경로가 잘못됨</li>
                    <li>XML 파일의 문법 오류</li>
                </ul>
                <p><strong>해결 방법:</strong> 브라우저 개발자 도구(F12)의 Console 탭에서 자세한 로그를 확인하세요.</p>
            </div>`;
    }
}

// 페이지 로드 후 실행
document.addEventListener('DOMContentLoaded', init);