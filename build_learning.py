"""Build focused algorithm additions while preserving existing site routes and anchors."""
from pathlib import Path
import re
from learning_content import translator,pqc_body,shor_body,grover_body,summary_rows,table,refs,SOURCES
ROOT=Path(__file__).resolve().parent

def href(page,lang):return page+('.zh' if lang=='zh' else '')+'.html'
def stylesheet(s):
    if 'href="learning.css"' not in s:s=s.replace('</head>','<link rel="stylesheet" href="learning.css"/></head>')
    return s

def replace_section(s,ident,body):
    s,n=re.subn(r'<section\b[^>]*id="'+ident+r'".*?</section>',lambda _:body,s,flags=re.S)
    assert n==1,(ident,n)
    return s

def main():
    for lang in ('en','zh'):
        t=translator(lang);zh=lang=='zh';home=href('index',lang);guide=href('quantum-guide',lang);detail=href('pqc-algorithms',lang)
        langs=''.join(f'<a data-atlas-lang="{code}" href="{href("pqc-algorithms",code)}" '+('aria-current="page"' if code==lang else '')+'>'+label+'</a>' for code,label in [('en','EN'),('zh','中文')])
        jumps=[('landscape',t('Overview','全景')),('ml-kem','ML-KEM'),('ml-dsa','ML-DSA'),('slh-dsa','SLH-DSA'),('fn-dsa','FN-DSA / Falcon'),('hqc','HQC'),('stateful','LMS / XMSS'),('comparison',t('Implementation review','实现审查'))]
        page=f'''<!doctype html>
<html lang="{'zh-CN' if zh else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#10182d"><meta name="description" content="{t('Six PQC algorithm families explained with original diagrams: ML-KEM, ML-DSA, SLH-DSA, Falcon/FN-DSA, HQC, LMS/XMSS; mechanisms, implementation boundaries and standards.','六类 PQC 算法原理与原创图解：ML-KEM、ML-DSA、SLH-DSA、Falcon/FN-DSA、HQC、LMS/XMSS；计算流程、实现边界与标准状态。')}"><title>{t('PQC algorithm details','PQC 算法详解')} · Quantum / PQC Atlas</title><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="guide.css"><link rel="stylesheet" href="learning.css"><script src="language.js"></script></head>
<body class="guide-page algorithm-page"><nav id="atlas-langbar" aria-label="{t('Language selection','语言选择')}">{langs}</nav><a class="skip" href="#main">{t('Skip to content','跳至正文')}</a><header class="guide-topbar"><a class="guide-brand" href="{home}">Q+ <span>QUANTUM / PQC ATLAS</span></a><a href="{guide}#shor">Shor / Grover ↗</a></header><main id="main"><section class="guide-hero"><span class="eyebrow">PQC / MECHANISMS / IMPLEMENTATION</span><h1>{t('PQC has more than<br>one mathematical foundation','PQC 不止一种<br>数学基础')}</h1><p>{t('Six entries, from polynomial masks to trapdoor sampling, error-correcting codes and hash trees. Follow each mechanism before comparing its interfaces, state and deployment status.','从多项式掩码到陷门采样、纠错码和哈希树，逐项理解六类算法，再比较接口、状态管理及部署进度。')}</p><p class="algorithm-review">{t('Standards and linked specifications reviewed 5 November 2026. Equations and diagrams are teaching models, not cryptographic implementations.','标准及所链规范复核于 2026 年 11 月 5 日。公式和图解为教学模型，不是密码实现。')}</p><nav class="guide-jumps" aria-label="{t('On this page','本页目录')}">{''.join(f'<a href="#{ident}">{label}</a>' for ident,label in jumps)}</nav></section>{pqc_body(lang)}</main><footer class="guide-footer"><a href="{home}#standards">← {t('PQC landscape','PQC 全景')}</a><span>{t('Original diagrams · No account or external script required','原创图解 · 无需账号或外部脚本')}</span><a href="{guide}#grover">Grover ↗</a></footer></body></html>'''
        page=re.sub(r'&(?!#\d+;|#x[0-9a-fA-F]+;|[A-Za-z]+;)', '&amp;',page)
        (ROOT/detail).write_text(page,encoding='utf-8')

        path=ROOT/guide;s=path.read_text()
        s=replace_section(s,'shor',shor_body(lang));s=replace_section(s,'grover',grover_body(lang))
        s=stylesheet(s)
        if 'src="algorithm-labs.mjs"' not in s:s=s.replace('</head>','<script type="module" src="algorithm-labs.mjs"></script></head>')
        if f'href="{detail}"' not in s:
            s=s.replace('</nav></section>',f'<a href="{detail}">PQC '+t('algorithm details','算法详解')+' ↗</a></nav></section>',1)
        # Fix broken ket characters in the earlier English translation without changing the circuit.
        if not zh:
            for ket in ('q₀q₁','00','01','10','11','0','1'):s=s.replace('|'+ket+'　','|'+ket+'⟩')
            s=s.replace('basiss','bases').replace('quick overview of grids and LWE','quick overview of lattices and LWE')
            s=s.replace('This site only provides introductory links; in-depth content on grids, LWE, attacks and parameter selection can be found in separate topics.','This site explains primitive workflows; lattice mathematics, LWE, attacks and parameter selection are explored in the separate lattice atlas.')
        else:s=s.replace('本站只给出入门连接；格、LWE、攻击与参数选择的深入内容见独立专题。','本站详解原语流程；格数学、LWE、攻击与参数选择的深入内容见独立格密码专题。')
        marker='<!-- PQC DETAIL LINK -->'
        if marker not in s:
            target='<section class="guide-section" id="reading">'
            pos=s.index(target)
            last=s.rfind('</section>',0,pos)
            s=s[:last]+marker+f'<p class="guide-next"><a href="{detail}">'+t('Read all six PQC families: Falcon, HQC and stateful hash signatures included ↗','继续阅读六类 PQC 算法：包括 Falcon、HQC 与有状态哈希签名 ↗')+'</a></p>'+s[last:]
        if 'Shor / Grover / PQC · 2026.11.05' not in s:
            s=s.replace('</footer>','<span>Shor / Grover / PQC · 2026.11.05</span></footer>')
        s=re.sub(r'&(?!#\d+;|#x[0-9a-fA-F]+;|[A-Za-z]+;)', '&amp;',s)
        path.write_text(s,encoding='utf-8')

        path=ROOT/home;s=path.read_text();s=stylesheet(s)
        cards=[('203','ML-KEM','ml-kem',t('Module-lattice KEM','模格 KEM'),t('KeyGen, encapsulation, implicit rejection and protocol authentication','密钥生成、封装、隐式拒绝与协议认证'),True),('204','ML-DSA','ml-dsa',t('Module-lattice signature','模格签名'),t('Fiat–Shamir, masked response, rejection bounds and hints','Fiat–Shamir、掩码响应、拒绝边界与 hint'),True),('205','SLH-DSA','slh-dsa',t('Stateless hash-based signature','无状态哈希签名'),t('FORS, WOTS+ and a hypertree; no persistent leaf counter','FORS、WOTS+ 与超树；无需持久化叶计数'),True),('fn','FN-DSA / Falcon','fn-dsa',t('NTRU lattice signature','NTRU 格签名'),t('Trapdoor Gaussian sampling; compact signatures, demanding implementation','陷门高斯采样；签名紧凑，实现要求高'),False),('hqc','HQC','hqc',t('Code-based KEM','编码型 KEM'),t('Sparse masks, public error correction and a salted KEM transform','稀疏掩码、公开纠错与加盐 KEM 转换'),False),('208','LMS / XMSS','stateful',t('Stateful hash-based signature','有状态哈希签名'),t('One-time keys, Merkle paths and rollback-resistant signing state','一次性密钥、Merkle 路径与防回滚签名状态'),True)]
        tiles=[]
        for source,name,anchor,family,desc,final in cards:
            status=t('Published · 2024','已发布 · 2024') if source in ('203','204','205') else t('SP 800-208 · 2020','SP 800-208 · 2020') if source=='208' else t('In development','制定中') if source=='fn' else t('Selected · 2025','已选中 · 2025')
            label='FIPS '+source if source in ('203','204','205') else 'FIPS 206' if source=='fn' else 'HQC' if source=='hqc' else 'SP 800-208'
            tiles.append(f'<article class="standard-card"><div class="standard-top"><span>{label}</span><span class="badge {"ratified" if final else "work"}">{status}</span></div><h3>{name}</h3><p class="standard-full">{family}</p><p>{desc}</p><a href="{detail}#{anchor}">'+t('Mechanism and diagram ↗','原理与图解 ↗')+f'</a><a href="{SOURCES[source][1]}" target="_blank" rel="noopener noreferrer">'+t('Primary source ↗','一手资料 ↗')+'</a></article>')
        body='<section class="section-pad section-white" id="standards"><div class="section-head"><div><span class="section-kicker">04 / ALGORITHM FAMILIES</span><h2>'+t('PQC extends beyond<br>the first three FIPS standards','PQC 全景，<br>不止首批三个 FIPS')+'</h2></div><p>'+t('Compare KEMs and signatures across lattice, code-based and hash-based designs. Published standards, selected algorithms and work in progress have distinct status; reviewed 5 November 2026.','从格、纠错码和哈希三条路线比较 KEM 与签名，区分已发布、已选中及制定中状态；复核于 2026 年 11 月 5 日。')+'</p></div><div class="standard-grid">'+''.join(tiles)+'</div>'
        # Use the same six-row map as the detail chapter, with links into that chapter.
        rows=summary_rows(lang)
        rows=[[row[0].replace('href="#',f'href="{detail}#'),*row[1:]] for row in rows]
        body+='<div class="algorithm-standard-table">'+table([t('Algorithm','算法'),t('Task','用途'),t('Family','技术路线'),t('Status','标准状态'),t('Mechanism','机制')],rows)+'</div>'
        body+=refs(lang,'nist','208')+'<div class="algorithm-quicklinks"><a href="'+detail+'">'+t('Six PQC families in depth ↗','六类 PQC 算法详解 ↗')+'</a><a href="'+guide+'#shor">Shor ↗</a><a href="'+guide+'#grover">Grover ↗</a></div><p>'+t('A KEM establishes a shared secret; a signature authenticates a message. Replacing one does not replace the other. The detailed chapter covers equations, diagrams, size examples and implementation boundaries.','KEM 用于建立共享秘密，签名用于认证消息，二者不能互相替代。详解页包含公式、图解、尺寸例子与实现边界。')+'</p></section>'
        s=replace_section(s,'standards',body)
        navlink=f'<a href="{detail}"><span>↗</span> '+t('PQC algorithm details','PQC 算法详解')+'</a>'
        if navlink not in s:s=s.replace(f'<a href="{guide}"><span>↗</span>',navlink+'\n'+f'<a href="{guide}"><span>↗</span>')
        marker='<!-- ALGORITHM DETAIL SHORTCUTS -->'
        if marker not in s:
            shortcuts=marker+'<div class="algorithm-quicklinks"><a href="'+guide+'#shor">'+t('Shor: period finding and phase estimation ↗','Shor：求阶与相位估计 ↗')+'</a><a href="'+guide+'#grover">'+t('Grover: amplitude amplification and local model ↗','Grover：振幅放大与本地模型 ↗')+'</a></div>'
            pos=s.index('<section class="section-pad section-ink" id="impact">');end=s.index('</section>',pos);s=s[:end]+shortcuts+s[end:]
        # Date this focused update, without relabeling older unrelated migration material as newly reviewed.
        if 'PQC / Shor / Grover: 2026.11.05' not in s:s=s.replace('</div>\n</aside>','<br/>PQC / Shor / Grover: 2026.11.05</div>\n</aside>') if '</div>\n</aside>' in s else s
        s=s.replace('</span><br/>PQC / Shor / Grover: 2026.11.05','<br/>PQC / Shor / Grover: 2026.11.05</span>')
        s=re.sub(r'&(?!#\d+;|#x[0-9a-fA-F]+;|[A-Za-z]+;)', '&amp;',s)
        path.write_text(s,encoding='utf-8')
    print('Built 2 PQC detail pages; integrated six-family maps and expanded Shor/Grover in both languages')
if __name__=='__main__':main()
