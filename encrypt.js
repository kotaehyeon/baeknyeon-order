// catalog-wip.json 의 products 를 패스프레이즈로 AES-GCM 암호화 -> enc.json
// 사용: node encrypt.js <비밀번호>
// 브라우저 WebCrypto 와 동일 포맷(PBKDF2-SHA256 + AES-GCM)으로 만들어 그대로 복호화 가능.
const crypto = require("crypto").webcrypto;
const fs = require("fs");
const path = require("path");

(async () => {
  const pass = process.argv[2];
  if (!pass) { console.error("비밀번호를 인자로 주세요: node encrypt.js <pw>"); process.exit(1); }
  const root = __dirname;
  const products = JSON.parse(fs.readFileSync(path.join(root, "catalog-wip.json"), "utf8")).products;
  const plain = JSON.stringify(products);

  const enc = new TextEncoder();
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const iter = 150000;
  const km = await crypto.subtle.importKey("raw", enc.encode(pass), "PBKDF2", false, ["deriveKey"]);
  const key = await crypto.subtle.deriveKey(
    { name: "PBKDF2", salt, iterations: iter, hash: "SHA-256" },
    km, { name: "AES-GCM", length: 256 }, false, ["encrypt"]);
  const ct = await crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, enc.encode(plain));

  const b64 = (b) => Buffer.from(b).toString("base64");
  const out = { salt: b64(salt), iv: b64(iv), ct: b64(new Uint8Array(ct)), iter, n: products.length };
  fs.writeFileSync(path.join(root, "enc.json"), JSON.stringify(out));
  console.log(`encrypted ${products.length} products, plain ${plain.length} chars -> ct ${out.ct.length} b64 chars`);
})();
