`lecture-basic\problem-renderer\problem-xmls\practice-{{argument}}.xml` 파일을 작성한다.

형식은 `.claude\template-problems.xml` 파일을 따른다.

내용은 사용자 지시를 따름.

## 각 요소별 CDATA 처리
각 요소 사이는 CDATA 처리하여 파싱 오류를 방지한다.

## 지켜야 할 사항
1. `<code>` 요소 내용으로 결과 테스트 코드를 넣지 않는다.
2. 주석을 넣지 않는다.
3. 함수 이름은 apple, mango 등 과일 이름으로 난독화한다.
4. hint는 사용자의 구체적 지시가 있으면 그때만 추가하고 평소에는 비워둔다.
5. 변수 이름은 a, b, c, x1, x2, y, w 등 적절한 단순 문자로 난독화한다.