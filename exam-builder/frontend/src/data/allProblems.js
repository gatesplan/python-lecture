// 이 폴더의 problems-*.json 파일을 자동으로 모두 읽어들인다.
// 새 문제 파일을 추가하면 별도 등록 없이 자동 포함된다(파일명 오름차순 정렬).
// 같은 id가 여러 파일에 있으면 먼저 읽힌 것만 유지한다(중복 제거).
const modules = import.meta.glob('./problems-*.json', { eager: true })

const seen = new Set()
export const allProblems = []
for (const key of Object.keys(modules).sort()) {
  for (const problem of modules[key].default) {
    if (problem.id && seen.has(problem.id)) continue
    if (problem.id) seen.add(problem.id)
    allProblems.push(problem)
  }
}
