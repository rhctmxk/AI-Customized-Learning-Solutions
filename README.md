# AI 맞춤형 학습 솔루션


# 💁서비스 소개
AI 기반의 다양한 기능을 통하여 학습자가 자격증을 원할하게 취득할 수 있도록 도와주는 웹 서비스입니다.<br>
COVID-19로 인한 비대면 생활로 인해 전통적인 교육의 개념이 크게 변화하였고 공교육에서도 온라인 수업이 본격적으로 적용되고 있으며 이에따라 학생들도 자기주도 학습 시간이 더 많아질 수밖에 없었다.<p>
그에 따라 자기 주도적 학습에 적응하기 힘든 학생들을 위해 AI 기술을 접목한 맞춤형 교육 플랫폼을 제공하여 보다, 창의력을 키우고 비판적인 사고력을 기르며, 문제해결능력 및 소통과 협업 능력 등 다양한 능력을 키울 수 있게 된다.<p>
본 서비스는 자격증 취득을 목표로 공부할 때 학습자 개인 역량에 맞춰진 커리큘럼을 제공한다. 한명 한명에게 최선의 트렌드를 반영한 양질의 콘텐츠를 제공하여 합격률을 향상시킬 수 있을 것으로 기대된다.
<br><br>

# 📂프로젝트 구성

### 아키텍처(Architecture)
<img width="4800" height="800" alt="아키텍처" src="https://user-images.githubusercontent.com/97437403/204820576-aaeb03ba-78b5-499a-b1ed-15d33a62abc0.png"><br><br><br>

# 📅개발 기간
22.04 ~ 22.11<br><br><br>


# 💫서비스 설명
### 메인 홈
<img width="1000" height="600" alt="아키텍처" src="https://user-images.githubusercontent.com/97437403/204820831-628aedc4-a4ab-49e0-8414-db3f1be092e6.png">
AYU 시스템 메인 페이지입니다.<br><br><br<br><br>


### 게시판
<img width="1000" height="600" alt="아키텍처" src="https://user-images.githubusercontent.com/97437403/204823182-8777beb0-f1cd-48f1-b62b-c489ea2a453f.png"><br><br>

### 자격증 선택
<img width="1000" height="600" alt="아키텍처" src="https://user-images.githubusercontent.com/97437403/204821361-c50f3d9f-addd-4e32-bae0-5a0be906c9ba.png">
수많은 자격증들 중에서 사용자가 원하는 자격증을 고르는 곳입니다.<br><br><br<br><br>


### 선택한 자격증
<img width="1000" height="600" alt="아키텍처" src="https://user-images.githubusercontent.com/97437403/204821559-065b12c6-b8fd-407c-9d70-366155116f25.png">
자격증을 선택하면 자격증에 대한 설명이 나오며 찜하기를 누르면 해당 자격증을 스터디할 수 있습니다.<br><br><br<br><br>


### 마이페이지(자격증 확인)
<img width="1000" height="600" alt="아키텍처" src="https://user-images.githubusercontent.com/97437403/204822063-d6634372-bb09-49eb-96f1-ea7710444733.png">
마이페이지에 선택한 자격증이 나옵니다.<br><br><br<br><br>


### 스터디 페이지
<img width="1000" height="600" alt="아키텍처" src="https://user-images.githubusercontent.com/97437403/204822542-cfd4aeb8-5547-40c1-bc3c-4e9650369826.png">
다양한 스터디로 학습이 가능합니다.<br><br><br<br><br>


### 이론스터디
<img width="1000" height="600" alt="아키텍처" src="https://user-images.githubusercontent.com/97437403/204822838-19959704-39cd-4aa1-b0a8-54d69b1ffa1f.png">
자격증 이론 PDF 창을 띄어 직접 필기할 수 있습니다.<br><br><br<br><br>


### 그룹스터디
<img width="1000" height="600" alt="아키텍처" src="https://user-images.githubusercontent.com/97437403/204822838-19959704-39cd-4aa1-b0a8-54d69b1ffa1f.png">
그룹 스터디는 학습자가 같이 공부할 사람을 구할 수 있는 기능이다. 게시판 형태로 만들 것이며, 스터디장이 방을 만들면 그 외의 사람들이 해당 방에 스터디 참가 신청을 할 수 있습니다.<br><br><br<br><br>


### 문제풀이
<img width="1000" height="600" alt="아키텍처" src="https://user-images.githubusercontent.com/97437403/204823976-a73fe78d-c031-4ea8-a002-59fdc1f18862.png">
웹캠을 이용하여 학습자의 얼굴을 인식해 현재 어떤 컨디션 인지, 집중을 잘하고 있는지 확인도 하며 자격증별 기출문제나 학습자별 해당 자격증에 대해 학습한 레벨에 맞게 문제를 풀어볼 수 있고 자신의 해당 자격증에 대한 학습 레벨을 테스트할 수 있다.<br<br><br><br<br><br>


### 유사문제 업로드
<img width="600" height="600" alt="아키텍처" src="https://user-images.githubusercontent.com/97437403/204824491-c5cc621a-6634-499a-934f-712ed8baabb3.png">
유사문제 업로드 모듈은 OCR 기능을 이용해서 사용자가 업로드한 사진의 텍스트를 추출함. 추출한 텍스트를 딥러닝 서버로 보내서 분석한 다음에 다시 장고 서버로 분석한 내용을 보내주면서 학습자가 올린 문제와 비슷한 문제를 추천해주는 기능이다.
