"""Public/private objects, data flow and readable pseudocode for seven PQC schemes.

Pseudocode is original teaching notation: packed encodings, validated hash helpers and
addressed tree operations are named rather than replaced with insecure toy primitives.
"""
from html import escape
from learning_diagrams import figure,node

def tr(lang):return lambda en,zh:zh if lang=='zh' else en
def code(value):return '<code>'+escape(value)+'</code>'
def paragraph(value):return '<p>'+escape(value)+'</p>'
def field_table(lang,rows):
 t=tr(lang)
 heads=[t('Object / visibility','对象 / 可见性'),t('Contents','包含什么'),t('Meaning','各字段的作用')]
 return '<div class="algorithm-table-wrap object-table" tabindex="0"><table class="algorithm-table"><thead><tr>'+''.join('<th scope="col">'+h+'</th>' for h in heads)+'</tr></thead><tbody>'+''.join('<tr><th scope="row">'+label+'</th><td>'+code(value)+'</td><td>'+explanation+'</td></tr>' for label,value,explanation in rows)+'</tbody></table></div>'

def operations(lang,ident,items):
 t=tr(lang);html='<div class="pqc-operations"><h3>'+t('Pseudocode: follow the inputs and outputs','伪代码：沿输入与输出阅读')+'</h3>'+paragraph(t('Expand each operation. Key generation is open initially; the other two operations are available below. Helpers retain the specification’s hashing, validation, encoding and parameter rules.','逐项展开阅读。默认显示密钥生成，其余两步可在下方展开。辅助函数仍须遵守规范的哈希、验证、编码和参数规则。'))
 for i,(name,inputs,outputs,body) in enumerate(items,1):
  html+=f'<details class="pqc-operation" id="{ident}-{name.lower()}"'+(' open' if i==1 else '')+f'><summary>{i:02} · {name}</summary><dl class="operation-io"><dt>'+t('Input','输入')+'</dt><dd>'+escape(inputs)+'</dd><dt>'+t('Output','输出')+'</dt><dd>'+escape(outputs)+'</dd></dl><pre tabindex="0" aria-label="'+escape(ident+' '+name+' '+t('pseudocode','伪代码'),quote=True)+'"><code>'+escape(body.strip())+'</code></pre></details>'
 return html+'</div>'

def object_figure(lang,ident,name,public,private,wire,kem=False):
 t=tr(lang)
 if kem:
  left=t('Sender uses the public key','发送方使用公钥');left_text='Encaps(ek) → (K, c)'
  right=t('Recipient uses the private key','接收方使用私钥');right_text='Decaps(dk, c) → K′'
  caption=t('KeyGen creates both keys. Only c is returned to the key owner; K and K′ remain local. KEMs do not produce a digital signature.','KeyGen 生成两把密钥。只向密钥持有者回传 c，K 与 K′ 留在各自本地。KEM 不产生数字签名。')
 else:
  left=t('Signer uses the private key','签名方使用私钥');left_text='Sign(sk, M, ctx) → σ' if ident in ('ml-dsa','slh-dsa') else 'Sign(sk, M) → sig'
  right=t('Verifier uses the public key','验证方使用公钥');right_text='Verify(pk, M, ctx, σ) → true / false' if ident in ('ml-dsa','slh-dsa') else 'Verify(pk, M, sig) → true / false'
  caption=t('KeyGen creates both keys. The signature and message may be public. Verification returns a decision; it does not recover a hidden plaintext or require the private key.','KeyGen 生成两把密钥。签名和消息可以公开；验证只输出是否接受，不负责恢复隐藏明文，也不需要私钥。')
 body='<div class="pqc-key-pair">'+node(t('PUBLIC · ek','公开 · ek') if kem else t('PUBLIC · pk','公开 · pk'),escape(public),'accent')+node(t('PRIVATE · dk','保密保存 · dk') if kem else t('PRIVATE · sk','保密保存 · sk'),escape(private),'caution')+'</div>'
 body+='<div class="pqc-object-transfer">'+node(left,left_text)+node(t('Sent over the protocol','通过协议传输'),escape(wire),'artifact')+node(right,right_text)+'</div>'
 return figure(lang,'objects-'+ident,name+' · '+t('keys, transmitted object and result','密钥、传输对象与结果'),body,caption)

SPECS={
 'ml-kem':('FIPS 203 · §§5–7','https://csrc.nist.gov/pubs/fips/203/final'),
 'ml-dsa':('FIPS 204 · §§5–7','https://csrc.nist.gov/pubs/fips/204/final'),
 'slh-dsa':('FIPS 205 · §§9–10','https://csrc.nist.gov/pubs/fips/205/final'),
 'fn-dsa':('Falcon v1.2 · §§3.4, 3.8–3.10','https://falcon-sign.info/falcon.pdf'),
 'hqc':('HQC 2026-10-12 · §§3.6–3.7','https://pqc-hqc.org/doc/hqc_specifications_2026_10_12.pdf'),
 'lms':('RFC 8554 · §§4–5','https://www.rfc-editor.org/rfc/rfc8554'),
 'xmss':('RFC 8391 · §§4.1, 4.2','https://www.rfc-editor.org/rfc/rfc8391')}

def intro(lang):
 t=tr(lang)
 body='<div class="pqc-reading-key"><h3>'+t('First identify the objects','先弄清这些对象是什么')+'</h3>'
 body+=paragraph(t('A public key is a structured value, not necessarily one number or curve point. A private-key container may also cache public fields. A signature is a separate output, not an encrypted private key. The tuples below describe contents; Pack/Encode produces the actual standardized byte string.','公钥是有结构的数据，不一定是一个整数或曲线点。私钥容器也可能缓存公开字段；签名是另一个计算输出，并不是“加密后的私钥”。下文的元组表示包含的内容，Pack/Encode 才生成规范规定的字节串。'))
 body+=field_table(lang,[(t('KEM: ML-KEM / HQC','KEM：ML-KEM / HQC'),'KeyGen → (ek, dk); Encaps(ek) → (K, c); Decaps(dk, c) → K′',t('ek is public; dk is private. Transmit ciphertext c, not shared secret K. There is no signature output.','ek 公开，dk 私有；传输的是密文 c，不是共享秘密 K；没有签名输出。')),(t('Digital signatures','数字签名'),'KeyGen → (pk, sk); Sign(sk, M) → σ; Verify(pk, M, σ) → bool',t('pk is public; sk is private. Send the message M with its signature σ. A protocol must separately establish whose public key it is.','pk 公开，sk 私有；消息 M 与签名 σ 一同交给验证方。公钥属于谁，仍须由协议另行认证。'))])
 body+=paragraph(t('Notation: || means byte-string concatenation; a hat marks an NTT representation; M is an application message, while m inside a KEM is fresh internal randomness. The same letter can mean different things in different algorithms. All examples assume a fixed, agreed parameter set. H/G/J/PRF are the specification’s distinct functions, not arbitrary replacements.','记号：|| 表示字节串拼接，帽号表示 NTT 表示；M 是应用消息，KEM 中的 m 则是新鲜内部随机值。同一字母在不同算法中可能含义不同。所有例子都假设事先确定参数组；H/G/J/PRF 是规范中不同的函数，不能任意替换。'))
 return body+'</div>'

def scheme(lang,ident):
 t=tr(lang)
 pub=t('Public key · public','公钥 · 可公开');sec=t('Private key · keep private','私钥 · 保密保存');sig=t('Signature · may be public','签名 · 可公开');ct=t('Ciphertext · transmitted','密文 · 传输');key=t('Shared secret · not sent','共享秘密 · 不传输')
 if ident=='ml-kem':
  name='ML-KEM';public='ek = Encode(t̂) || ρ';private='dk = dkPKE || ek || H(ek) || z';wire='c = Pack(Compress(u), Compress(v))'
  lead=t('The recipient owns ek and dk. Anyone holding the authenticated ek can encapsulate a fresh secret to that recipient. dk is a complete decapsulation bundle, not just the small secret vector.','接收方持有 ek 与 dk，任何获得已认证 ek 的发送方都可以向其封装新鲜秘密。dk 是完整解封密钥包，并非只有一个小秘密向量。')
  rows=[(pub,public,t('ρ expands the public matrix A; t̂ is the NTT encoding of t=As+e. A need not be sent in full.','ρ 用于展开公开矩阵 A；t̂ 是 t=As+e 的 NTT 编码，不必传输完整 A。')),(sec,private,t('dkPKE encodes ŝ. Cached ek and H(ek) support re-encryption; secret z produces the implicit-rejection key.','dkPKE 编码 ŝ；缓存的 ek 与 H(ek) 用于重加密，秘密 z 用于生成隐式拒绝密钥。')),(ct,'c = c1 || c2 = Pack(Compress(u), Compress(v))',t('u is a polynomial vector and v a polynomial. This is a KEM ciphertext, not a signature or application-data ciphertext.','u 是多项式向量，v 是多项式；这是 KEM 密文，不是签名，也不是业务数据密文。')),(key,'K / K′: 32 bytes',t('On an honestly generated ciphertext both parties obtain the same K; failed re-encryption selects a fallback key.','诚实生成的密文使两端得到相同 K；重加密校验失败时选择回退密钥。'))]
  ops=[('KeyGen',t('Parameter set and secure randomness','参数组与安全随机源'),'(ek, dk)', '''d, z ← RandomBytes(32), RandomBytes(32)
(ρ, noiseSeed) ← G(d || U8(k))
Â ← ExpandA(ρ)
(s, e) ← SamplePKESecrets(noiseSeed, parameters)
ŝ ← NTT(s); t̂ ← MatVecNTT(Â, ŝ) + NTT(e)
ek ← Encode12(t̂) || ρ
dkPKE ← Encode12(ŝ)
dk ← dkPKE || ek || H(ek) || z
return (ek, dk)'''),('Encaps','ek','(K, c)', '''CheckEncapsulationKey(ek)
m ← RandomBytes(32)
(K, coins) ← G(m || H(ek))
(t̂, ρ) ← DecodePKEPublicKey(ek); Â ← ExpandA(ρ)
(r, e₁, e₂) ← SampleEncryptionNoise(coins, parameters)
u ← InverseNTT(MatVecNTT(Transpose(Â), NTT(r))) + e₁
v ← InverseNTT(DotNTT(t̂, NTT(r))) + e₂ + EncodeMessage(m)
c ← PackCompressed(u, v, parameters)
return (K, c)'''),('Decaps','dk, c','K′', '''CheckDecapsulationInputs(dk, c)
(dkPKE, ek, hek, z) ← Parse(dk)
ŝ ← Decode12(dkPKE); (u, v) ← UnpackDecompress(c)
m′ ← DecodeMessage(v − InverseNTT(DotNTT(ŝ, NTT(u))))
(Kgood, coins′) ← G(m′ || hek)
c′ ← K-PKE.Encrypt(ek, m′, coins′)
Kbad ← J(z || c)
return ConstantTimeSelect(c′ == c, Kgood, Kbad)''')]
  note=t('K-PKE is the internal polynomial encryption mechanism explained below. MatVecNTT/DotNTT apply the standard’s NTT-domain ring products; matrix expansion, noise counters and compression follow FIPS 203; it is not an independent public encryption API. The displayed dk is the expanded standard form; permitted seed-based storage is a representation choice, not a different KEM.','K-PKE 是下文解释的内部多项式加密机制；MatVecNTT/DotNTT 按标准执行 NTT 域环乘法；矩阵展开、噪声计数器及压缩均遵循 FIPS 203，不能作为独立公开加密 API。这里展示标准展开 dk；规范允许的种子存储是表示方式选择，不是另一个 KEM。')
 elif ident=='ml-dsa':
  name='ML-DSA';public='pk = Pack(ρ, t₁)';private='sk = Pack(ρ, K, tr, s₁, s₂, t₀)';wire='M, σ = Pack(c̃, z, hint); ctx agreed'
  lead=t('The public key contains a matrix seed and rounded public vector. The signature contains a challenge digest, a masked response and correction hints. The verifier recreates the challenge; it does not receive the signing mask y or the secret vectors.','公钥包含矩阵种子和舍入后的公开向量；签名包含挑战摘要、掩码响应和纠正 hint。验证方重建挑战，不会获得签名掩码 y 或秘密向量。')
  rows=[(pub,public,t('ρ expands A; t=As₁+s₂ is split as t=2^d·t₁+t₀ by Power2Round. Only t₁ goes in pk.','ρ 展开 A；Power2Round 将 t=As₁+s₂ 分为 t=2^d·t₁+t₀，公钥只携带 t₁。')),(sec,private,t('s₁,s₂ are small secret vectors; t₀ is the low part. K is a secret mask-derivation seed, not a KEM shared secret. tr=H(pk) is a cached public-key hash.','s₁、s₂ 是小秘密向量，t₀ 是低位部分；K 是秘密掩码派生种子，不是 KEM 共享秘密；tr=H(pk) 是缓存的公钥哈希。')),(sig,'σ = (c̃, z, hint)',t('c̃ is the hash challenge digest, mapped by SampleInBall to polynomial c. z=y+c·s₁; hint is a sparse bit vector. Neither y nor c as a full polynomial is transmitted.','c̃ 是挑战哈希摘要，经 SampleInBall 映射为多项式 c；z=y+c·s₁；hint 是稀疏比特向量。不会传输 y 或完整多项式 c。')),(t('Message and context','消息与上下文'),'M, ctx; μ = H(tr || EncodePure(ctx, M))',t('ctx and the pure/prehash mode must agree. μ is an internal representative, not an extra signature field.','ctx 及 pure/prehash 模式必须一致；μ 是内部消息代表值，不是额外的签名字段。'))]
  ops=[('KeyGen',t('Parameter set and secure seed','参数组与安全种子'),'(pk, sk)', '''(ρ, ρ′, K) ← ExpandKeySeed(RandomBytes(32), parameters)
A ← ExpandA(ρ)
(s₁, s₂) ← ExpandS(ρ′)
t ← A*s₁ + s₂
(t₁, t₀) ← Power2Round(t)
pk ← Pack(ρ, t₁); tr ← H(pk)
sk ← Pack(ρ, K, tr, s₁, s₂, t₀)
return (pk, sk)'''),('Sign','sk, M, ctx','σ', '''(ρ, K, tr, s₁, s₂, t₀) ← DecodeSK(sk)
μ ← H(tr || EncodePure(ctx, M))
maskSeed ← H(K || SigningRandomizer() || μ)
A ← ExpandA(ρ); counter ← 0
repeat:
    y ← ExpandMask(maskSeed, counter); counter ← counter + l
    w ← A*y; w₁ ← HighBits(w)
    c̃ ← ChallengeHash(μ || Encode(w₁)); c ← SampleInBall(c̃)
    z ← y + c*s₁
    r₀ ← LowBits(w − c*s₂)
    if ||z||∞ ≥ γ₁−β or ||r₀||∞ ≥ γ₂−β: continue
    if ||c*t₀||∞ ≥ γ₂: continue
    hint ← MakeHint(−c*t₀, w − c*s₂ + c*t₀)
    if Weight(hint) > ω: continue
    return Pack(c̃, z, hint)'''),('Verify','pk, M, ctx, σ',t('true / false','接受 / 拒绝'), '''(ρ, t₁), (c̃, z, hint) ← StrictDecode(pk, σ)
if bad encoding or ||z||∞ ≥ γ₁−β or Weight(hint) > ω: return false
μ ← H(H(pk) || EncodePure(ctx, M))
c ← SampleInBall(c̃); A ← ExpandA(ρ)
w′ ← A*z − c*(2^d*t₁)
w₁′ ← UseHint(hint, w′)
return c̃ == ChallengeHash(μ || Encode(w₁′))''')]
  note=t('All polynomial products above are mathematical products modulo q; NTT representations are hidden for readability, so ExpandA denotes the corresponding coefficient-space matrix here. γ₁/γ₂, β and ω are the parameter-set response/rounding bounds, safety margin and maximum hint weight; norms are centered coefficient infinity norms. SigningRandomizer is the standard hedged randomizer, or its specified zero value for deterministic signing. ChallengeHash, packing and pure-mode context encoding have the exact FIPS-defined lengths.','以上乘法为模 q 的数学多项式乘法，为便于阅读省略 NTT 表示，此处 ExpandA 表示对应的系数域矩阵。γ₁/γ₂、β、ω 是参数组给出的响应/舍入边界、安全余量和最大 hint 重量；范数为中心化系数无穷范数。SigningRandomizer 使用标准对冲随机值，或确定性变体规定的零值；挑战哈希、打包及 pure 模式上下文编码的长度均由 FIPS 规定。')
 elif ident=='slh-dsa':
  name='SLH-DSA';public='PK = (PK.seed, PK.root)';private='SK = (SK.seed, SK.prf, PK.seed, PK.root)';wire='M, SIG = R || SIG_FORS || SIG_HT; ctx agreed'
  lead=t('The public key is a public hash seed plus the top Merkle root. The private key adds two secret seeds. A signature is a collection of hash-based proofs connecting the message to that root; it is not the root alone.','公钥由公开哈希种子与顶层 Merkle 根组成；私钥额外包含两个秘密种子。签名是一组将消息连接到该根的哈希证明材料，不是仅有一个根值。')
  rows=[(pub,public,t('PK.seed configures addressed public hash operations; PK.root is the trusted top-level root. Both are public n-byte strings.','PK.seed 用于带地址的公开哈希运算，PK.root 是可信顶层根；两者均为公开 n 字节串。')),(sec,private,t('SK.seed derives FORS/WOTS+ secret elements. SK.prf generates message randomization R. The public fields are copied into SK for use during signing.','SK.seed 派生 FORS/WOTS+ 秘密元素；SK.prf 用于生成消息随机化值 R；SK 缓存公开字段以便签名。')),(sig,'SIG = R || SIG_FORS || SIG_HT',t('R is public randomization data; SIG_FORS holds selected secrets and their paths; SIG_HT holds each layer’s WOTS+ signature and authentication path.','R 是公开随机化数据；SIG_FORS 包含选中秘密值与路径；SIG_HT 包含各层 WOTS+ 签名及认证路径。')),(t('Internal indices','内部索引'),'(md, idx_tree, idx_leaf) = Split(H_msg(...))',t('The verifier derives the indices from R, PK and M; they are not an independent monotonic counter carried between signing calls.','验证方由 R、PK 与 M 重算索引；它们不是签名调用间持续递增的状态计数器。'))]
  ops=[('KeyGen',t('Parameter set and secure randomness','参数组与安全随机源'),'(PK, SK)', '''SK.seed, SK.prf, PK.seed ← RandomN(), RandomN(), RandomN()
PK.root ← TopHypertreeRoot(SK.seed, PK.seed)
PK ← (PK.seed, PK.root)
SK ← (SK.seed, SK.prf, PK.seed, PK.root)
return (PK, SK)'''),('Sign','SK, M, ctx','SIG', '''M′ ← EncodePure(ctx, M)
R ← PRF_msg(SK.prf, AdditionalRandomness(), M′)
digest ← H_msg(R, PK.seed, PK.root, M′)
(md, tree, leaf) ← SplitDigest(digest)
ADRS ← FORSAddress(tree, leaf)
SIG_FORS ← FORS.Sign(md, SK.seed, PK.seed, ADRS)
pkFORS ← FORS.PkFromSig(SIG_FORS, md, PK.seed, ADRS)
SIG_HT ← Hypertree.Sign(pkFORS, SK.seed, PK.seed, tree, leaf)
return R || SIG_FORS || SIG_HT'''),('Verify','PK, M, ctx, SIG',t('true / false','接受 / 拒绝'), '''(R, SIG_FORS, SIG_HT) ← StrictDecode(SIG, parameters)
M′ ← EncodePure(ctx, M)
(md, tree, leaf) ← SplitDigest(H_msg(R, PK.seed, PK.root, M′))
pkFORS ← FORS.PkFromSig(SIG_FORS, md, PK.seed, FORSAddress(tree, leaf))
root′ ← Hypertree.RootFromSig(pkFORS, SIG_HT, PK.seed, tree, leaf)
return root′ == PK.root''')]
  note=t('Hypertree.RootFromSig recovers each WOTS+ public key from its signature, follows its Merkle path, and uses that subtree root as the next layer’s message. Every call uses its specified layer/tree/keypair address. AdditionalRandomness is the standard random value, or PK.seed in the specified deterministic variant. No private leaf-use counter is introduced.','Hypertree.RootFromSig 逐层由签名恢复 WOTS+ 公钥、沿 Merkle 路径得到根，再把该根作为上一层的消息；每次调用必须使用规定的层、树及密钥对地址。AdditionalRandomness 为标准随机值，确定性变体则使用规定的 PK.seed；不引入私有已用叶计数器。')
 elif ident=='fn-dsa':
  name='Falcon / FN-DSA';public='pk = h = g/f mod (Xⁿ+1, q)';private='sk: f, g, F, G; fG − gF = q';wire='M, sig = (salt, Compress(s₂))'
  lead=t('This is the Falcon v1.2 submission design, used to explain FN-DSA’s origin. The public key is a polynomial h. The secret is a short NTRU basis; a signature sends a salt and one compressed short polynomial. It does not send that basis.','这里采用 Falcon v1.2 提交设计解释 FN-DSA 的来源。公钥是多项式 h，秘密为一组短 NTRU 基；签名传输盐值和一条压缩短多项式，不传输这组基。')
  rows=[(pub,public,t('A public polynomial modulo q in the agreed ring. Algorithm/degree identifiers accompany its encoded form.','约定环上模 q 的公开多项式，编码形式另带算法/次数标识。')),(sec,'(f, g, F, G); optional FFT basis and LDL tree',t('The conceptual trapdoor has four polynomials. Serialized secret keys can retain f,g,F and reconstruct G; expanded sampler data is secret too.','概念陷门包含四条多项式；序列化私钥可保存 f、g、F 并重建 G；展开的采样器数据同样属于秘密。')),(sig,'sig = (salt, EncodeCompressed(s₂))',t('salt chooses the public hash target c. Only s₂ is sent; the verifier computes centered s₁=c−s₂h mod q. The required headers and padding are encoding details.','salt 决定公开哈希目标 c；只传输 s₂，验证方计算中心化 s₁=c−s₂h mod q；规定的头部及填充另由编码处理。')),(t('Internal sampled pair','内部采样对'),'(s₁, s₂): s₁+s₂h=c mod q',t('Both polynomials must jointly satisfy the norm bound. s₁ is not an extra transmitted signature field.','两条多项式共同满足范数界；s₁ 不是额外传输的签名字段。'))]
  ops=[('KeyGen',t('Falcon parameter set and secure randomness','Falcon 参数组与安全随机源'),'(pk, sk)', '''repeat:
    (f, g) ← SampleSmallPolynomials()
    if not KeyGenerationBoundsPass(f, g): continue
    if f is not invertible modulo q: continue
    (F, G) ← SolveNTRU(f, g, q)
    if solve failed or required bounds fail: continue
    h ← g*f⁻¹ mod (X^n+1, q)
    return (h, (f, g, F, G))'''),('Sign','sk, M','sig', '''salt ← RandomBytes(40)
c ← HashToPoint(salt || M)
B, samplerTree ← ExpandTrapdoor(sk)
repeat:
    (s₁, s₂) ← GaussianPreimageSample(B, samplerTree, c)
    if ||(s₁, s₂)||² > bound: continue
    encoded ← CompressForSignatureFormat(s₂)
    if encoding does not fit: continue
    return PackSignature(salt, encoded)'''),('Verify','pk=h, M, sig',t('true / false','接受 / 拒绝'), '''(salt, encoded_s₂) ← StrictDecodeSignature(sig, parameters)
s₂ ← StrictDecompress(encoded_s₂)
c ← HashToPoint(salt || M)
s₁ ← CenteredRepresentative(c − s₂*h mod (X^n+1, q))
return ||(s₁, s₂)||² ≤ bound''')]
  note=t('The Gaussian sampler is a specified randomized trapdoor algorithm, not deterministic nearest-point rounding. FIPS 206 remains in development: these Falcon salt and encoding details must not be presented as a finalized FN-DSA wire format.','高斯采样器是规定的随机陷门算法，不是确定性最近点舍入。FIPS 206 仍在制定中，不能将这里的 Falcon 盐值和编码细节标成已定稿的 FN-DSA 传输格式。')
 elif ident=='hqc':
  name='HQC';public='ek = (seed_PKE.ek, s)';private='dk = seed_KEM (32 bytes)';wire='c_KEM = (u, v, salt)'
  lead=t('In the 2026-10-12 project specification, the stored KEM private key is a 32-byte master seed. Decapsulation expands it to recreate the PKE keys and rejection secret. Saying “the private key is y” describes only one expanded internal role, not this KEM’s stored key format.','在 2026-10-12 项目规范中，KEM 保存的私钥是 32 字节主种子。解封时展开它，重新生成 PKE 密钥及拒绝秘密。“私钥就是 y”只描述一个展开后的内部角色，不是这个 KEM 的存储密钥格式。')
  rows=[(pub,public,t('The public seed regenerates dense h; the public syndrome-like vector s=x+hy is sent explicitly.','公开种子重建稠密 h，公开关系向量 s=x+hy 则显式传输。')),(sec,'dk = seed_KEM; expanded: seed_PKE.dk, y, x, rejectSecret',t('A master-seed XOF stream supplies seed_PKE first, then rejectSecret. I(seed_PKE) gives the PKE secret/public seeds, from which x,y,h are derived.','主种子的 XOF 流先给出 seed_PKE，再给出 rejectSecret；I(seed_PKE) 产生 PKE 秘密/公开种子，再据此派生 x、y、h。')),(ct,'c_KEM = ((u,v), salt)',t('u and v are the PKE ciphertext; salt is public and binds encapsulation derivation. No digital-signature tag is added.','u、v 是 PKE 密文，salt 公开并参与封装派生；不额外附加数字签名标签。')),(key,'K = 32 bytes; m has parameter-dependent length',t('G splits into shared key K and encryption coins θ. K is retained locally. The specification’s rejection-secret symbol is not a signature.','G 的输出拆为共享密钥 K 与加密随机性 θ，K 留在本地。规范中拒绝秘密使用的符号并不表示签名。'))]
  ops=[('KeyGen',t('HQC parameter set and secure randomness','HQC 参数组与安全随机源'),'(ek, dk)', '''seed_KEM ← RandomBytes(32)
stream ← XOF.Init(seed_KEM)
seed_PKE ← stream.Take(32)
(seed_dk, seed_ek) ← I(seed_PKE)
(y, x) ← SecretFixedWeightSamples(seed_dk)
h ← PublicVector(seed_ek)
s ← x + h*y
ek ← (seed_ek, s); dk ← seed_KEM
return (ek, dk)'''),('Encaps','ek','(K, c_KEM)', '''CheckEncapsulationInput(ek)
m ← RandomBytes(MessageBytes)
salt ← RandomBytes(SaltBytes)
(K, θ) ← G(H(Encode(ek)) || m || salt)
(u,v) ← HQC-PKE.Encrypt(ek, m, θ)
return (K, ((u,v), salt))'''),('Decaps','dk=seed_KEM, c_KEM','K′', '''CheckDecapsulationInputs(dk, c_KEM)
stream ← XOF.Init(dk); seed_PKE ← stream.Take(32)
(ekPKE, dkPKE) ← HQC-PKE.KeyGen(seed_PKE)
rejectSecret ← stream.Take(MessageBytes)
((u,v), salt) ← Parse(c_KEM)
(m′, decode_ok) ← DecodeCandidate(dkPKE, (u,v))
(Kgood, θ′) ← G(H(Encode(ekPKE)) || m′ || salt)
c′ ← (HQC-PKE.Encrypt(ekPKE, m′, θ′), salt)
Kbad ← J(H(Encode(ekPKE)) || rejectSecret || Encode(c_KEM))
ok ← decode_ok and (Encode(c′) == Encode(c_KEM))
return ConstantTimeSelect(ok, Kgood, Kbad)''')]
  note=t('HQC-PKE samples fixed-weight r₂,e,r₁ from θ, computes u=r₁+hr₂ and v=C(m)+T(sr₂+e); decryption regenerates y and decodes v−T(uy). The helper ordering and domain separation follow the dated project specification. Decoder failure handling must preserve implicit-rejection semantics without a secret-dependent error oracle; DecodeCandidate supplies fixed-length dummy candidate bytes and a false flag on decoding failure, so only the fallback key can be selected.','HQC-PKE 按 θ 采样定重 r₂、e、r₁，计算 u=r₁+hr₂、v=C(m)+T(sr₂+e)；解密重建 y，并解码 v−T(uy)。辅助函数的顺序和域分离遵循所注明日期的项目规范。解码失败须保持隐式拒绝语义，不能暴露秘密相关错误 Oracle；DecodeCandidate 在解码失败时提供定长占位候选和失败标志，因此最终只能选择回退密钥。')
 elif ident=='lms':
  name='LMS';public='pk = (lms_type, ots_type, I, T[1])';private='sk ≈ (secret SEED, q, I, parameters)';wire='M, sig = (q, LMOTS_sig, lms_type, auth)'
  lead=t('LMS authenticates an LM-OTS public key with a Merkle root. The tree root and identifier I are public. The secret generation material and next-unused leaf q stay with the signer; q is state that must advance durably.','LMS 用 Merkle 根认证 LM-OTS 公钥。树根和标识 I 公开；秘密生成材料及下一未用叶 q 保留在签名端，q 是必须持久化递增的状态。')
  rows=[(pub,public,t('Algorithm types fix the hash and tree/chain parameters. I is the 16-byte tree identifier; T[1] is the Merkle root.','算法类型确定哈希、树和链参数；I 是 16 字节树标识，T[1] 是 Merkle 根。')),(sec,'secret SEED (or explicit LM-OTS keys), next q, tree data',t('RFC 8554 does not mandate one private-key serialization. A pseudorandom seed representation is shown here; traversal caches are implementation-specific.','RFC 8554 不强制唯一私钥序列化格式；这里展示伪随机种子表示，遍历缓存由实现决定。')),(sig,'q || (ots_type, C, y[0…p−1]) || lms_type || auth[0…h−1]',t('C randomizes the message digest. Each y[i] is an intermediate hash-chain value; auth contains sibling nodes from leaf q to the root.','C 随机化消息摘要；每个 y[i] 是哈希链中间值；auth 是叶 q 通向根的兄弟节点。')),(t('State / capacity','状态 / 容量'),'0 ≤ q < 2^h',t('One distinct-message signing slot per leaf. Publishing q in a signature is safe; allocating it twice is not.','每叶只提供一个不同消息签名槽位；签名中公开 q 是安全的，重复分配 q 则不安全。'))]
  ops=[('KeyGen',t('Approved LMS/LM-OTS parameters and randomness','获批 LMS/LM-OTS 参数与随机源'),'(pk, stateful sk)', '''SEED ← SecureSeed(); I ← RandomBytes(16)
for each q in 0…2^h−1:
    Kq ← LMOTS.PublicKeyFromSeed(SEED, I, q)
    leaf[q] ← LMS.LeafHash(I, q, Kq)
T ← LMS.BuildMerkleTree(I, leaf)
sk ← (SEED, next_q=0, I, parameters)
pk ← (lms_type, ots_type, I, T[1])
return (pk, sk)'''),('Sign','stateful sk, M',t('Updated state and signature','已更新状态与签名'), '''q ← ReserveUnusedLeafDurably(sk)
if exhausted: return FAIL
C ← RandomN()
Q ← H(I || U32(q) || U16(D_MESG) || C || M)
digits ← WinternitzDigitsWithChecksum(Q, ots_type)
y ← LMOTS.ChainSign(SEED, I, q, digits)
auth ← LMS.AuthenticationPath(I, q)
return Updated(sk), Pack(q, ots_type, C, y, lms_type, auth)'''),('Verify','pk, M, sig',t('true / false','接受 / 拒绝'), '''(q, ots_type, C, y, lms_type, auth) ← StrictDecode(sig)
if types mismatch or q ≥ 2^h or wrong lengths: return false
Q ← H(I || U32(q) || U16(D_MESG) || C || M)
digits ← WinternitzDigitsWithChecksum(Q, ots_type)
Kq′ ← LMOTS.PublicKeyFromSignature(I, q, digits, y)
leaf′ ← LMS.LeafHash(I, q, Kq′)
root′ ← LMS.RootFromPath(I, q, leaf′, auth)
return root′ == T[1]''')]
  note=t('LM-OTS signing derives each secret chain start, then hashes forward by the corresponding message/checksum digit. Verification continues from the disclosed value to the public chain endpoint and hashes all endpoints into Kq′. LMS leaf/internal hashes include I, node numbers and domain constants; they are not a generic unlabelled binary tree. ReserveUnusedLeafDurably must never return the same q after concurrency, crash or rollback.','LM-OTS 签名先派生各链秘密起点，再按消息/校验和数字向前哈希；验证从揭示值继续哈希到公开链端点，将所有端点哈希成 Kq′。LMS 叶/内部哈希包含 I、节点号及域常量，不是没有标签的普通二叉树。ReserveUnusedLeafDurably 在并发、崩溃或回滚后也绝不能返回重复 q。')
 elif ident=='xmss':
  name='XMSS';public='pk = (OID, root, PUB_SEED)';private='sk ≈ (idx, SK_SEED, SK_PRF, root, PUB_SEED)';wire='M, sig = (idx_sig, r, WOTS_sig, auth)'
  lead=t('XMSS uses WOTS+ rather than LM-OTS. It has secret OTS-generation material, a separate secret PRF key and a public seed for addressed hashes/masks. Here PUB_SEED names the public SEED of RFC 8391 so it cannot be confused with LMS’s private seed.','XMSS 使用 WOTS+，而不是 LM-OTS。它具有秘密 OTS 生成材料、另一把秘密 PRF 密钥，以及用于带地址哈希/掩码的公开种子。这里把 RFC 8391 的公开 SEED 写为 PUB_SEED，避免与 LMS 的私有种子混淆。')
  rows=[(pub,public,t('OID identifies the parameter set; root authenticates the tree; PUB_SEED is public input for address-dependent hash operations.','OID 标识参数组，root 认证整棵树，PUB_SEED 是依赖地址的哈希运算公开输入。')),(sec,'next idx, SK_SEED (or explicit WOTS+ keys), SK_PRF, root, PUB_SEED',t('This is a pseudorandom-key representation. RFC 8391 also describes explicit WOTS+ private keys. The mutable index and optional traversal state are part of the signing system.','这是伪随机密钥表示；RFC 8391 也描述显式保存 WOTS+ 私钥的形式。可变索引及可选遍历状态都属于签名系统。')),(sig,'idx_sig || r || WOTS_sig || auth',t('r is a public per-index PRF output. WOTS_sig contains chain values; auth authenticates the L-tree-compressed WOTS+ public key.','r 是每个索引对应的公开 PRF 输出；WOTS_sig 包含链值；auth 认证经 L-tree 压缩的 WOTS+ 公钥。')),(t('Hash input / address','哈希输入 / 地址'),'digest = H_msg(r || root || IndexBytes(idx_sig), M)',t('The message digest binds r, the public root and the index. Layer/tree/OTS/chain addresses select distinct hash invocations.','消息摘要绑定 r、公开根和索引；层、树、OTS、链地址区分不同哈希调用。'))]
  ops=[('KeyGen',t('Approved XMSS parameters and randomness','获批 XMSS 参数与随机源'),'(pk, stateful sk)', '''SK_SEED, SK_PRF, PUB_SEED ← SecureSeed(), RandomN(), RandomN()
for each q in 0…2^h−1:
    wots_pk[q] ← WOTS.PublicKey(SK_SEED, q, PUB_SEED, ADRS(q))
    leaf[q] ← LTree(wots_pk[q], PUB_SEED, ADRS(q))
root ← XMSS.TreeRoot(leaf, PUB_SEED)
sk ← (next_idx=0, SK_SEED, SK_PRF, root, PUB_SEED)
pk ← (OID, root, PUB_SEED)
return (pk, sk)'''),('Sign','stateful sk, M',t('Updated state and signature','已更新状态与签名'), '''q ← ReserveUnusedLeafDurably(sk)
if exhausted: return FAIL
r ← PRF(SK_PRF, ToBytes(q, 32))
digest ← H_msg(r || root || ToBytes(q, n), M)
WOTS_sig ← WOTS.Sign(digest, SK_SEED, PUB_SEED, ADRS(q))
auth ← XMSS.AuthenticationPath(q, PUB_SEED)
return Updated(sk), Pack(q, r, WOTS_sig, auth)'''),('Verify','pk, M, sig',t('true / false','接受 / 拒绝'), '''(q, r, WOTS_sig, auth) ← StrictDecode(sig, OID)
if q ≥ 2^h or wrong lengths: return false
digest ← H_msg(r || root || ToBytes(q, n), M)
wots_pk′ ← WOTS.PublicKeyFromSig(digest, WOTS_sig, PUB_SEED, ADRS(q))
leaf′ ← LTree(wots_pk′, PUB_SEED, ADRS(q))
root′ ← XMSS.RootFromPath(leaf′, auth, q, PUB_SEED, ADRS(q))
return root′ == root''')]
  note=t('WOTS+ includes the checksum, masked hash chains and address rules; LTree compresses its multiple public chain endpoints into one Merkle leaf. idx in the signature is public; the signer’s next_idx is durable allocation state. These single-tree pseudocodes do not stand in for the full HSS/XMSSMT hierarchy. LMS’s w counts bits per digit, while WOTS+ uses w as a base: the same symbol is not an interchangeable parameter.','WOTS+ 包含校验和、带掩码的哈希链及地址规则；LTree 把多条公开链端点压缩成一个 Merkle 叶。签名中的 idx 公开，签名端 next_idx 则是持久分配状态。这些单树伪代码不能代替完整 HSS/XMSSMT 层级。LMS 的 w 表示每数字位数，WOTS+ 的 w 表示基数，同名符号不能直接互换参数。')
 else:raise KeyError(ident)
 body=f'<article class="pqc-protocol" id="interface-{ident}" data-scheme="{ident}"><h3>{name} · '+t('objects and operations','对象与操作')+'</h3>'+paragraph(lead)
 body+=object_figure(lang,ident,name,public,private,wire,ident in ('ml-kem','hqc'))
 body+=field_table(lang,rows)+operations(lang,ident,ops)+paragraph(note)
 label,url=SPECS[ident]
 body+='<p class="algorithm-references">'+t('Pseudocode reference: ','伪代码依据：')+f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label} ↗</a></p></article>'
 return body

def interfaces(lang,ident):
 t=tr(lang)
 if ident=='landscape':return intro(lang)
 if ident=='stateful':
  return '<div class="algorithm-quicklinks"><a href="#interface-lms">LMS</a><a href="#interface-xmss">XMSS</a></div>'+scheme(lang,'lms')+scheme(lang,'xmss')+'<h3>'+t('Shared Merkle-tree and state-management principles','共有的 Merkle 树与状态管理原理')+'</h3>'
 if ident in SPECS:return scheme(lang,ident)+'<h3>'+t('Why the mechanism works','机制为什么成立')+'</h3>'
 return ''
