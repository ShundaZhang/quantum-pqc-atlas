# Quantum / PQC Atlas

面向软件与安全工程师的中文学习网站：从量子计算的最小模型、Shor / Grover 的密码威胁，到 NIST 抗量子密码标准及系统迁移。

网站：https://shundazhang.github.io/quantum-pqc-atlas/

纯静态页面，无第三方脚本或构建依赖。使用任意静态文件服务器即可本地预览，例如在本目录运行 `python3 -m http.server 8000`，然后打开 `http://localhost:8000/`。

[站内知识导读](quantum-guide.html)吸收两个公开仓库中的知识介绍：量子基础、实验输出、纠缠应用、Shor / Grover、算法地图与 BB84；格与 LWE 只作简明速览，深入内容留给后续独立专题。无需外部量子平台账号。本地 Bell 实验运行 `python3 labs/bell_state.py`，只使用 Python 标准库。外部课程仅作为可选延伸阅读。

[代码实验路径](code-labs.html)把 `quantum-computing-python-samples` 和 `lattice-based-cryptography-samples` 两个公开仓库编成六个关卡；网站提供运行步骤和实验边界，仓库继续维护源码。

格密码已有独立的[格密码地图](https://shundazhang.github.io/lattice-crypto-atlas/)，本网站保留一页速览并引导深入。

内容最后核对：2026-09-24。标准与协议状态可能变化，请以网站中的一手资料链接为准。

## Algorithm expansion - 2026-11-05

- [PQC algorithm details](pqc-algorithms.html) / [Chinese](pqc-algorithms.zh.html): ML-KEM, ML-DSA, SLH-DSA, FN-DSA/Falcon, HQC, LMS/XMSS; mechanisms, diagrams, current status and implementation boundaries.
- Expanded the existing Shor/Grover guide sections, preserving their bookmarks.
- 18 original bilingual diagrams (including seven key/output object diagrams) and two local teaching models: ideal phase-sample postprocessing and exact Grover amplitudes/probabilities. Neither connects to quantum hardware or implements a cryptanalytic attack.
- HQC follows the project specification of 2026-10-12. FIPS 206 remains in development; HQC selection is distinguished from publication of a NIST standard. LMS/XMSS are linked to SP 800-208 and RFC 8554/8391.

Build the additions with `python3 -B build_learning.py` (standard library only). Run model tests with `node --test tests/algorithm-models.test.mjs`. Older, unrelated chapters retain their own review dates.

## Explicit key and output structures

Each of ML-KEM, ML-DSA, SLH-DSA, Falcon, HQC, LMS and XMSS now has its own public/private/output diagram, field-by-field table and KeyGen plus two-operation pseudocode. LMS and XMSS are separate subsections with their own state and signature formats. The 21 pseudocode operations use native disclosure controls: KeyGen is initially open, and encapsulation/signing plus decapsulation/verification can be expanded. Pseudocode is pedagogical and keeps specification-defined encodings, validation, domain separation and helper routines explicit.
