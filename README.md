# 백년양말 폰 발주 웹앱

폰에서 색상별 수량(죽)을 누르면 카카오톡에 붙여넣을 발주서 텍스트가 자동 생성되는 단일 페이지 웹앱.

- **발주서 형식**: `제품명 / 사이즈 / 색상 / N죽`
- **가격표 보호**: 카탈로그(제품·가격)는 비밀번호로 AES-GCM 암호화되어 `index.html`에 들어감.
  공개 저장소에도 암호문만 올라가므로 비밀번호 없이는 가격을 볼 수 없음.
- **호스팅**: GitHub Pages (`index.html` 루트 서빙)

## 카탈로그가 바뀌었을 때 (월 1~2회)

1. `catalog-wip.json` 의 제품 데이터를 수정 (이 파일은 평문이라 저장소에 올라가지 않음 — 로컬 보관)
2. 재암호화 → 재빌드 → 푸시:
   ```
   node encrypt.js <비밀번호>
   python3 build.py
   git add index.html && git commit -m "카탈로그 갱신" && git push
   ```
3. 같은 주소에서 자동 반영 (폰에서 새로 할 것 없음)

## 비밀번호 변경

`node encrypt.js <새비밀번호>` → `python3 build.py` → 커밋·푸시. 폰에서 새 비번 한 번 입력.

## 파일

- `index.html` — 배포되는 앱 (암호화된 카탈로그 포함)
- `catalog-wip.json` — 평문 카탈로그 원본 (gitignore, 로컬 전용)
- `encrypt.js` — 카탈로그 암호화 도구
- `build.py` — `enc.json` → `index.html` 생성
- `docs/superpowers/specs/` — 설계서
