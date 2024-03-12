export const summer = [
    {
      "id": "system-prompt-1",
      "role": "system",
      "content": "As a student who's just beginning to dive into web development, I'd like to understand how to create a simple website featuring cat pictures. Please respond in Korean."
    },
    {
      "id": "user-prompt-1",
      "role": "user",
      "content": "고양이 사진이 있는 간단한 웹사이트 프로젝트에 대한 글, 동기"
    },
    {
      "id": "assistant-prompt-1",
      "role": "assistant",
      "content": [
        { "insert": "고양이 갤러리 웹사이트 만들기: 동기", "attributes": { "bold": true } },
        { "insert": "첫 프로젝트로 고양이 사진이 특징인 간단한 웹사이트를 만들고 싶어 합니다. 이 과정을 통해 JSON 응답을 이해하고자 합니다." }
      ]
    }
  ]

export const winter = [
    {
      "id": "system-prompt-2",
      "role": "system",
      "content": "As a member of the coding club, I want to share a new project idea using JSON format. This project will involve creating an interactive website. Please respond in Korean."
    },
    {
      "id": "user-prompt-2",
      "role": "user",
      "content": "JSON 포맷을 사용하여 상호작용하는 웹사이트를 만드는 프로젝트, 본문을 작성하고자 합니다."
    },
    {
      "id": "assistant-prompt-2",
      "role": "assistant",
      "content": [
        { "insert": "인터랙티브 웹사이트 프로젝트: ", "attributes": { "bold": true } },
        { "insert": "JSON 포맷을 사용하여 사용자 상호작용을 강화하는 웹사이트를 만들고자 합니다.." },
        { "insert": "먼저 JSON을 직렬화 하는 방법에 대해 고민해볼수 있습니다." },
      ]
    }
  ]


  export const validQuillContentPrompt = `This format illustrates how to encapsulate a comprehensive web experience within JSON responses, using an example structure like [{ "insert": "The importance of JSON responses: ", "attributes": { "bold": true } }, { "insert": "JSON responses must include HTML, CSS, and JavaScript to ensure a full-fledged web experience. Accurately escaping special characters and providing a detailed description of the content is necessary. Moreover, the use of promise chaining for efficiently managing large datasets and incorporating a placeholder to denote the continuation of data retrieval in subsequent requests is highlighted. This approach is fundamental in delivering rich, interactive web content methodically and seamlessly across multiple requests." }]. The inclusion of HTML, CSS, and JavaScript is emphasized to ensure a complete web experience, along with the accurate escape of special characters and the provision of a detailed content description. Furthermore, it underscores the importance of using promise chaining for efficient data management and embedding a placeholder for ongoing data retrieval, which are crucial for providing a systematic and smooth delivery of rich, interactive web content across multiple requests.`;
