"""Original, bilingual, dependency-free diagrams for PQC and quantum algorithms."""
from html import escape

def figure(lang,ident,title,body,caption):
    t=lambda en,zh:zh if lang=='zh' else en
    return f'<figure class="learning-figure" aria-labelledby="{ident}-title"><span class="figure-tag">{t("ORIGINAL VISUAL GUIDE","原创图解")}</span><h3 id="{ident}-title">{title}</h3>{body}<figcaption>{caption}</figcaption></figure>'

def node(title,text='',tone=''):
    return f'<div class="learning-node {tone}"><strong>{title}</strong><span>{text}</span></div>'

def flow(items):
    return '<div class="learning-flow">'+''.join(node(a,b,tone) for a,b,tone in items)+'</div>'

def svgframe(lang,ident,title,content,caption,viewbox='0 0 900 270'):
    return figure(lang,ident,title,'<div class="diagram-scroll" tabindex="0"><svg class="wide-diagram" viewBox="'+viewbox+'" role="img" aria-label="'+escape(title,quote=True)+'"><defs><marker id="'+ident+'-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#376b76"/></marker></defs>'+content+'</svg></div>',caption)

def diagram(lang,ident):
    t=lambda en,zh:zh if lang=='zh' else en
    if ident=='pqc-map':
        body='<div class="learning-split"><div>'+node('KEM',t('Establish a shared secret','建立共享秘密'),'accent')+flow([('ML-KEM',t('Module-LWE','模格 / Module-LWE'),''),('HQC',t('Quasi-cyclic code problems','准循环编码问题'),'')])+'</div><div>'+node(t('Digital signature','数字签名'),t('Authenticate a message','认证消息'),'accent')+'<div class="learning-branches">'+node('ML-DSA / FN-DSA',t('Lattice signatures','格基签名'))+node('SLH-DSA',t('Stateless hash-based','无状态哈希'))+node('LMS / XMSS',t('Stateful hash-based','有状态哈希'),'caution')+'</div></div></div>'
        return figure(lang,ident,t('Start with the task, then choose the mathematical family','先分用途，再分数学路线'),body,t('KEMs and signatures are not interchangeable. “Hash-based” does not by itself tell you whether persistent signing state is required.','KEM 与签名不能互换。“基于哈希”本身不能说明是否需要持久化签名状态。'))
    if ident=='mlkem-flow':
        body=flow([(t('Recipient · KeyGen','接收方 · KeyGen'),t('Keep dk; publish ek','保留 dk；公开 ek'),''),(t('Sender · Encaps(ek)','发送方 · Encaps(ek)'),t('Fresh hidden m → (c, K)','新鲜的内部随机消息 m → (c, K)'),'accent'),(t('Recipient · Decaps(dk,c)','接收方 · Decaps(dk,c)'),t('Recover m′; re-encrypt and compare','恢复 m′；重加密并比较'),'')])+node(t('Only c travels back; K remains local at both ends','只回传 c；两端各自保留 K'),t('Protocol KDF + authenticated encryption protect application data','协议 KDF + 认证加密保护业务数据'),'accent')
        return figure(lang,ident,t('ML-KEM: re-encryption is part of the KEM, not an optional check','ML-KEM：重加密校验是 KEM 的组成部分'),body,t('The public key must be authenticated by the surrounding protocol. This diagram omits encoding, compression and the internal hash functions.','公钥认证由外围协议完成。图中省略编码、压缩及内部哈希函数。'))
    if ident=='mldsa-flow':
        body=flow([(t('Commit','承诺'),'y → w = Ay → w₁ = HighBits(w)',''),(t('Challenge','挑战'),'c ← SampleInBall(H(μ, w₁))','accent'),(t('Respond + reject','响应 + 拒绝采样'),'z = y + cs₁; bounds + hints','')])+node(t('Verify','验证'),t('Reconstruct high bits from Az − c·2ᵈt₁ and hints; recompute c','由 Az − c·2ᵈt₁ 与 hint 重建高位，再计算 c'),'accent')
        return figure(lang,ident,t('ML-DSA: Fiat–Shamir with aborts','ML-DSA：带拒绝采样的 Fiat–Shamir'),body,t('Arrows describe data dependence. A rejected signing attempt samples another mask; implementations must follow every bound and domain-separation rule.','箭头表示数据依赖。被拒绝的签名尝试须重新取掩码；实现必须遵守全部边界及域分离规则。'))
    if ident=='slh-flow':
        body=flow([(t('Message digest','消息摘要'),t('R + message + public key → indices','R + 消息 + 公钥 → 索引'),''),('FORS',t('Reveal selected secrets + authentication paths','揭示选中秘密值 + 认证路径'),'accent'),('WOTS+ / XMSS',t('Sign FORS public key at the bottom layer','底层签署 FORS 公钥'),'')])+node(t('Hypertree: sign subtree roots up to the public root','超树：逐层签署子树根，直至公开根'),t('Verify FORS → WOTS+ chains → Merkle paths → PK.root','验证 FORS → WOTS+ 链 → Merkle 路径 → PK.root'),'accent')
        return figure(lang,ident,t('SLH-DSA: a forest authenticated by a hypertree','SLH-DSA：用超树认证一片森林'),body,t('Conceptual layering, not the number of actual trees. Stateless operation depends on the complete construction and parameter limits, not on freely reusing a one-time key.','展示概念层次，不代表实际树的数量。无状态安全依赖完整构造和参数限制，不代表一次性密钥可以任意复用。'))
    if ident=='falcon-flow':
        body=flow([(t('Hash to a target','哈希到目标点'),'c = HashToPoint(salt, M)',''),(t('Trapdoor sampling','陷门采样'),t('Secret NTRU basis → short (s₁,s₂)','秘密 NTRU 基 → 短向量 (s₁,s₂)'),'accent'),(t('Public verification','公开验证'),'s₁ + s₂h = c mod q; norm bound','')])
        return figure(lang,ident,t('Falcon: a short preimage of a public target','Falcon：寻找公开目标的短原像'),body,t('Falcon submission-level algebra. The wire signature compresses s₂ and includes a salt; the verifier reconstructs s₁. Future FN-DSA encoding must follow its own specification.','Falcon 提交版的代数示意。实际签名压缩 s₂ 并包含盐值，验证方重建 s₁；FN-DSA 编码须以其正式规范为准。'))
    if ident=='hqc-flow':
        body=flow([(t('Encode','编码'),'m → Reed–Solomon → repeated Reed–Muller',''),(t('Mask with sparse noise','稀疏噪声掩蔽'),'u = r₁ + hr₂; v = C(m) + T(sr₂ + e)','accent'),(t('Cancel + decode','抵消 + 解码'),'v − T(uy) → noisy codeword → m′','')])+node(t('KEM wrapper','KEM 外层'),t('Salted FO transform · re-encryption check · implicit rejection','加盐 FO 转换 · 重加密校验 · 隐式拒绝'),'accent')
        return figure(lang,ident,t('HQC: correct the noise after cancelling the secret mask','HQC：抵消秘密掩码后纠错'),body,t('T denotes the specified truncation. Binary addition and subtraction are XOR. This is a structural diagram of the 2026-10-12 project specification, not a FIPS standard.','T 表示规范规定的截断。二进制加减均为 XOR。以 2026-10-12 项目规范作结构示意，并非 FIPS 标准。'))
    if ident=='merkle-path':
        body='<g class="tree-lines"><path d="M450 75L240 135M450 75L660 135M240 165L120 225M240 165L340 225M660 165L560 225M660 165L780 225"/></g>'
        for x,y,w,label,tone in [(350,20,200,t('Public root','公开根'),'accent'),(145,125,190,'H(L₀,L₁)','caution'),(565,125,190,'H(L₂,L₃)','accent'),(40,215,160,'L₀',''),(260,215,160,'L₁',''),(480,215,160,t('L₂ · chosen leaf','L₂ · 当前叶'),'accent'),(700,215,160,'L₃','caution')]:
            body+=f'<g class="svg-node {tone}"><rect x="{x}" y="{y}" width="{w}" height="46" rx="6"/><text x="{x+w/2}" y="{y+29}" text-anchor="middle">{label}</text></g>'
        return svgframe(lang,ident,t('One Merkle root authenticates many one-time public keys','一个 Merkle 根认证多个一次性公钥'),body,t('For leaf 2, the authentication path contains L₃ and H(L₀,L₁). The signature provides the OTS signature and index; the verifier recovers the chosen leaf, then hashes upward in index-dependent order. Four leaves are a teaching example.','叶 2 的认证路径为 L₃ 和 H(L₀,L₁)。签名携带 OTS 签名和索引；验证方恢复当前叶，再按索引决定的顺序向上哈希。四叶树仅为教学例子。'))
    if ident=='state-flow':
        body=flow([(t('Reserve leaf q','预留叶 q'),t('Atomic allocation; persist q+1','原子分配；持久化 q+1'),'caution'),(t('Sign with OTS q','用 OTS q 签名'),t('Never give q to another request','绝不把 q 分给另一请求'),'accent'),(t('Release the signature','返回签名'),t('Crash may waste q; must not reuse it','崩溃可浪费 q，不能重用 q'),'')])+node(t('Rollback / cloned signer → repeated q → forgery risk','回滚 / 克隆签名端 → 重复 q → 伪造风险'),t('A verifier need not maintain the signer’s counter','验证方不需要维护签名端计数器'),'caution')
        return figure(lang,ident,t('LMS / XMSS: persistent state is part of the security boundary','LMS / XMSS：持久状态属于安全边界'),body,t('This conservative reservation model illustrates crash safety. Hardware profiles, multi-tree traversal and distributed state allocation require additional specification-specific controls.','这是说明崩溃安全的保守预留模型。硬件配置、多树遍历及分布式状态分配仍须遵循各自规范。'))
    if ident=='shor-flow':
        body=flow([(t('Classical preprocessing','经典预处理'),'N; choose a; gcd(a,N)',''),(t('Quantum order finding','量子求阶'),'controlled U²ʲ → inverse QFT → c','accent'),(t('Classical postprocessing','经典后处理'),'c/Q → k/r → r → gcd(aʳᐟ² ± 1,N)','')])
        return figure(lang,ident,t('Shor combines classical number theory and quantum interference','Shor 结合经典数论与量子干涉'),body,t('Only the middle block is quantum. A measured phase need not reveal the full order; candidate periods and resulting factors must be checked.','只有中间部分是量子计算。一次测得的相位未必揭示完整阶；候选阶及因子都必须校验。'))
    if ident=='shor-circuit':
        body=''
        for y,label in [(68,t('t counting qubits','t 个计数位')),(185,t('work register |1⟩','工作寄存器 |1⟩'))]:
            body+=f'<text x="10" y="{y-20}" class="svg-small">{label}</text><path class="circuit-wire" d="M150 {y}H870"/>'
        for x,y,w,label in [(160,42,95,'H⊗t'),(320,40,220,t('controlled U²ʲ','受控 U²ʲ')),(595,42,130,'QFT⁻¹'),(775,42,95,t('measure c','测量 c'))]:
            body+=f'<g class="svg-node"><rect x="{x}" y="{y}" width="{w}" height="54" rx="5"/><text x="{x+w/2}" y="{y+33}" text-anchor="middle">{label}</text></g>'
        body+='<path d="M430 95V158" class="circuit-control"/><g class="svg-node accent"><rect x="320" y="158" width="220" height="54" rx="5"/><text x="430" y="191" text-anchor="middle">U|y⟩ = |ay mod N⟩</text></g>'
        body+=f'<text x="160" y="248" class="svg-small">{t("N=15, a=2, Q=256: phase peaks at c=0,64,128,192","N=15、a=2、Q=256：相位峰位于 c=0、64、128、192")}</text>'
        return svgframe(lang,ident,t('Phase estimation extracts the order from modular multiplication','相位估计从模乘运算中提取阶'),body,t('A grouped circuit: controlled powers U^(2^j), j=0…t−1, replace one expanded gate row per counting qubit. U acts as identity on computational-basis values y≥N to complete a unitary. Physical gate decomposition and ancillas are omitted.','分组线路图：受控幂 U^(2^j)，j=0…t−1，概括各计数位的门序列。对 y≥N 的计算基态令 U 为恒等以补全酉运算。省略物理门分解及辅助位。'))
    if ident=='grover-flow':
        body=flow([(t('Uniform state','均匀态'),'H⊗n|0…0⟩ = |s⟩',''),(t('Phase oracle','相位 Oracle'),'O_f|x⟩ = (−1)^f(x)|x⟩','caution'),(t('Diffusion','扩散反射'),'D = 2|s⟩⟨s| − I','accent')])+node(t('Repeat D·O_f, then measure','重复 D·O_f，然后测量'),t('Stop near the first peak; more iterations can lower success','在首个峰值附近停止，继续迭代可能降低成功率'),'')
        return figure(lang,ident,t('Grover uses two reflections to rotate toward a marked state','Grover 用两次反射旋转到标记态'),body,t('A phase flip alone leaves measurement probabilities unchanged. The following diffusion converts that relative phase into a change in amplitudes.','仅翻转相位不会改变测量概率；之后的扩散反射才把相对相位转化为振幅变化。'))
    raise KeyError(ident)
