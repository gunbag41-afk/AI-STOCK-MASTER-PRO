AI STOCK MASTER PRO V1.8.0 — 서버 배포 준비본

실제 온라인 배포는 아직 수행되지 않았습니다.

휴대폰에서 HTML 파일만 실행할 경우: 모의투자, 예시 차트, CSV 분석 가능. 실제 주가 자동 조회 불가.

온라인 배포 (Render 예시):
1. ZIP 압축 해제 후 index.html, server.py, Dockerfile, .dockerignore, render.yaml을 GitHub 저장소 루트에 올립니다.
2. Render 계정에서 New > Web Service > GitHub 저장소를 연결합니다.
3. Docker 런타임으로 배포하고 HTTPS 주소를 확인합니다.
4. https://발급주소/api/health 에서 JSON 응답을 확인합니다.
5. 휴대폰에서 https://발급주소/ 로 접속한 후 실제 주가 불러오기를 시도합니다.

서버 연결 확인은 외부 주가 데이터 수신 성공과 다릅니다.
비공식 Yahoo Finance 차트 API는 접속 제한/변경될 수 있고 상업적 이용 권한이 확인되지 않았습니다.
실제 주문 기능 및 검증된 AI 상승 확률은 제공하지 않습니다.

V1.8.0 변경사항:
- 모바일 화면에 배포 절차를 펼쳐 볼 수 있는 안내 추가
- /api/health 버전 동기화
- 서버에서 /index.html 외 정적 파일 접근 차단 (server.py 등 노출 방지)
- 기존 모의투자 로컬 저장 키 유지
