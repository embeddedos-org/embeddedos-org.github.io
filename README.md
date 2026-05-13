# EoS — Embedded Operating System Developer Portal

<!-- BEGIN PLATFORMS -->
## v3.0.0 — Unified Production Release (2026-05-13)

All 18 EmbeddedOS-org repositories released at v3.0.0. Per-platform binaries are produced by each repo's `release.yml` workflow and attached to its GitHub Release.

| Repo | Release | Linux x64/arm64 | macOS x64/arm64 | Windows x64 | Docker | Other |
|---|---|---|---|---|---|---|
| [eos](https://github.com/embeddedos-org/eos/releases/tag/v3.0.0) | v3.0.0 | ELF/BIN per board (47 product profiles, AArch64/ARM-HF/RISC-V64) | — | — | ghcr.io/embeddedos-org/eos | mdBook · promo |
| [eAI](https://github.com/embeddedos-org/eAI/releases/tag/v3.0.0) | v3.0.0 | ✓ | ✓ | ✓ | ghcr.io/embeddedos-org/eai | Conan + vcpkg pkgs |
| [eIPC](https://github.com/embeddedos-org/eIPC/releases/tag/v3.0.0) | v3.0.0 | eipc-cli/-client/-server (linux/darwin/windows × amd64/arm64/armv7) | ✓ | ✓ | ghcr.io/embeddedos-org/eipc | C SDK static+shared |
| [eNI](https://github.com/embeddedos-org/eNI/releases/tag/v3.0.0) | v3.0.0 | core lib + eni-cli | ✓ | ✓ | ghcr.io/embeddedos-org/eni | Python wheel · Rust crate · Node SDK · Java AAR |
| [eBoot](https://github.com/embeddedos-org/eBoot/releases/tag/v3.0.0) | v3.0.0 | bootloader ELF/BIN per board (83 boards) | host eflash | host eflash | — | — |
| [eBrowser](https://github.com/embeddedos-org/eBrowser/releases/tag/v3.0.0) | v3.0.0 | ✓ | ✓ | MSI installer | ghcr.io/embeddedos-org/ebrowser | — |
| [eDB](https://github.com/embeddedos-org/eDB/releases/tag/v3.0.0) | v3.0.0 | wheel + sdist | wheel + sdist | wheel + sdist | ghcr.io/embeddedos-org/edb | standalone browser/edb.html |
| [eOffice](https://github.com/embeddedos-org/eOffice/releases/tag/v3.0.0) | v3.0.0 | .AppImage/.deb/.snap | .dmg | .exe | ghcr.io/embeddedos-org/eoffice | .vsix · .crx · .safariextz · PWA |
| [eVera](https://github.com/embeddedos-org/eVera/releases/tag/v3.0.0) | v3.0.0 | wheel + PyInstaller | dmg + wheel | exe + wheel | ghcr.io/embeddedos-org/evera | APK · AAB · IPA · .crx |
| [EoSim](https://github.com/embeddedos-org/EoSim/releases/tag/v3.0.0) | v3.0.0 | wheel + GUI binary | wheel + GUI binary | wheel + GUI binary | ghcr.io/embeddedos-org/eosim | platform packs |
| [EoStudio](https://github.com/embeddedos-org/EoStudio/releases/tag/v3.0.0) | v3.0.0 | wheel + GUI binary | wheel + GUI binary | wheel + GUI binary | ghcr.io/embeddedos-org/eostudio | promo MP4 |
| [eosllm](https://github.com/embeddedos-org/eosllm/releases/tag/v3.0.0) | v3.0.0 | eosllm-cli/-bench/-convert/-quant-lab/-server | ✓ | ✓ | — | .vsix · .crx · .xpi |
| [ebuild](https://github.com/embeddedos-org/ebuild/releases/tag/v3.0.0) | v3.0.0 | wheel + sdist + PyInstaller | ✓ | ✓ | — | SBOM |
| [eApps](https://github.com/embeddedos-org/eApps/releases/tag/v3.0.0) | v3.0.0 | native + Electron + APK + AAB + IPA | .dmg | .exe + .msi | — | .vsix · .crx · .xpi · .safariextz |
| [eFab](https://github.com/embeddedos-org/eFab/releases/tag/v3.0.0) | v3.0.0 | source tarball (manifest meta-repo) | — | — | — | eai-edge profile pinned to v3.0.0 |
| [eCAD-Hardware-Products](https://github.com/embeddedos-org/eCAD-Hardware-Products/releases/tag/v3.0.0) | v3.0.0 | source tarball + PDF datasheets | — | — | — | KiCad/3D assets |
| [embeddedos-org](https://github.com/embeddedos-org/embeddedos-org/releases/tag/v3.0.0) | v3.0.0 | source tarball | — | — | — | org index |
| [embeddedos-org.github.io](https://github.com/embeddedos-org/embeddedos-org.github.io/releases/tag/v3.0.0) | v3.0.0 | static site (this) | — | — | — | this download matrix |

Each release also includes: `<repo>-book-3.0.0.{pdf,epub,html.zip}` (mdBook), `<repo>_v3.0.0_promo.mp4` (promo video), `sbom.json` (CycloneDX), source tarball + zip.
<!-- END PLATFORMS -->


[![Deploy](https://github.com/embeddedos-org/embeddedos-org.github.io/actions/workflows/deploy.yml/badge.svg)](https://github.com/embeddedos-org/embeddedos-org.github.io/actions/workflows/deploy.yml)
[![CI](https://github.com/embeddedos-org/embeddedos-org.github.io/actions/workflows/ci.yml/badge.svg)](https://github.com/embeddedos-org/embeddedos-org.github.io/actions/workflows/ci.yml)
[![Scorecard](https://github.com/embeddedos-org/embeddedos-org.github.io/actions/workflows/scorecard.yml/badge.svg)](https://github.com/embeddedos-org/embeddedos-org.github.io/actions/workflows/scorecard.yml)

**Website**: [embeddedos-org.github.io](https://embeddedos-org.github.io)

**Foundation**: [embeddedos-org.github.io](https://embeddedos-org.github.io)

**App Store**: [embeddedos-org.github.io/eApps](https://embeddedos-org.github.io/eApps/)

## v0.1.0 Release

All repositories at v0.1.0 — a complete embedded AI systems stack.

### Ecosystem (13 Components)

| Repo | Description | Language | Version |
|---|---|---|---|
| [eos](https://github.com/embeddedos-org/eos) | Core OS — HAL (33 interface declarations; ARM Cortex-M kernel arch port + Linux host backend in production), RTOS kernel, multicore SMP/AMP API, services, GDB stub, core dump, loadable drivers, device tree parser | C11 | v0.1.0 |
| [eboot](https://github.com/embeddedos-org/eboot) | A/B embedded bootloader — STM32F4 production reference + 5 partial boards (rpi4, nrf52, stm32h7, samd51, x86_64_serial), A/B update with rollback, RFC&nbsp;8032 Ed25519 verification (vendored ed25519-donna), staged boot, recovery | C11 | v0.1.0 |
| [ebuild](https://github.com/embeddedos-org/ebuild) | Build system — SDK generator (14 targets), hardware analyzer, deliverable packager, 18 CLI commands | Python | v0.1.0 |
| [eipc](https://github.com/embeddedos-org/eipc) | Secure IPC — Go + C SDK, HMAC-SHA256, replay protection, TCP/Unix/SHM transports, priority lanes | Go + C | v0.1.0 |
| [eai](https://github.com/embeddedos-org/eai) | AI layer — llama.cpp, 12 LLM models, agent loop, LoRA fine-tuning, federated learning, 8-layer security | C11 | v0.1.0 |
| [eni](https://github.com/embeddedos-org/eni) | Neural interface — BCI, Neuralink adapter (1024ch/30kHz), DSP, neural net, intent decoder | C11 | v0.1.0 |
| [eApps](https://github.com/embeddedos-org/eApps) | **Unified App Store** — 60+ apps: 46 native, 32 mobile, 34 web, 20 browser ext, 14 dev tools, 22 CLI, 16 enterprise | Multi | v0.1.0 |
| [EoStudio](https://github.com/embeddedos-org/EoStudio) | Design suite — 12 editors (3D, CAD, UI, game, hardware), 30+ code generators, LLM integration | Python | v0.1.0 |
| [eosim](https://github.com/embeddedos-org/eosim) | Simulator — 52+ platforms, 12 architectures, EoSim native engine, QEMU/Renode/HIL | Python | v0.1.0 |
| [eDB](https://github.com/embeddedos-org/eDB) | Database — SQL + Document + Key-Value, REST API, JWT auth, AES-256, eBot AI queries | Python | v0.1.0 |
| [eBrowser](https://github.com/embeddedos-org/eBrowser) | Browser engine — HTML5/CSS rendering for embedded/IoT, modular architecture, plugin system | C | v0.1.0 |
| [eOffice](https://github.com/embeddedos-org/eOffice) | Office suite — 11 apps (eDocs, eSheets, eSlides, eMail, eDrive), eBot AI assistant | JS/TS | v0.1.0 |
| [eCAD-Hardware-Products](https://github.com/embeddedos-org/eCAD-Hardware-Products) | Hardware designs — KiCad PCBs, EE docs, board datasheets for reference products | KiCad | v0.1.0 |

### eApps — Unified Marketplace

All desktop/mobile/web/extension apps are consolidated in the [eApps](https://github.com/embeddedos-org/eApps) repository:

| Category | Count | Technologies | Delivery |
|---|---|---|---|
| Native Apps | 46 | C + LVGL | Binaries, WASM |
| Desktop Apps | 4 | Electron, Python, C/SDL2 | `.exe` `.dmg` `.AppImage` |
| Mobile Apps | 32 | Flutter | `.apk` `.aab` `.ipa` |
| Web Apps | 34 | HTML5/JS/WASM PWA | GitHub Pages |
| Browser Extensions | 20 | Manifest V3 | `.zip` `.crx` `.xpi` |
| Dev Tools | 14 | VS Code, JetBrains | `.vsix` `.jar` |
| CLI Tools | 22 | Node.js, Python | npm, pip |
| Enterprise | 16 | Docker, Helm, MSI | Images, charts |

🏪 **[Browse the App Store →](https://embeddedos-org.github.io/eApps/)**

### Supported Hardware (14 targets)

| Target | Arch | CPU | Vendor | Board |
|---|---|---|---|---|
| stm32f4 | ARM | Cortex-M4 | ST | STM32F407 |
| stm32h7 | ARM | Cortex-M7 | ST | STM32H743 |
| nrf52 | ARM | Cortex-M4 | Nordic | nRF52840 |
| rp2040 | ARM | Cortex-M0+ | RPi | RP2040 |
| raspi3 | AArch64 | Cortex-A53 | Broadcom | BCM2837 |
| raspi4 | AArch64 | Cortex-A72 | Broadcom | BCM2711 |
| imx8m | AArch64 | Cortex-A53 | NXP | i.MX8M |
| am64x | AArch64 | Cortex-A53 | TI | AM6442 |
| riscv_virt | RISC-V | rv64gc | QEMU | virt |
| sifive_u | RISC-V | U74 | SiFive | FU740 |
| esp32 | Xtensa | LX6 | Espressif | ESP32 |
| malta | MIPS | 24Kf | MIPS | Malta |
| x86_64 | x86_64 | generic | Generic | PC/Server |

### Build & Deploy

```bash
# Build the OS
cmake -B build -DEOS_PRODUCT=robot -DEOS_BUILD_TESTS=ON
cmake --build build && ctest --test-dir build

# Generate SDK for target
ebuild sdk --target raspi4

# Source environment and build app
source build/eos-sdk-raspi4/environment-setup
cmake -B build -DCMAKE_TOOLCHAIN_FILE=$CMAKE_TOOLCHAIN_FILE
cmake --build build

# Build eApps (60+ cross-platform apps)
cd eApps && cmake -B build -DEAPPS_PORT=sdl2 && cmake --build build

# Simulate without hardware
eosim run stm32f4 --timeout 30
```

### CI/CD

| Workflow | Schedule | Coverage |
|----------|----------|----------|
| **CI** | Every push/PR | Build + test on Linux × Windows × macOS |
| **Nightly** | 2:00 AM UTC daily | Full regression suite + cross-compile |
| **Weekly** | Monday 6:00 AM UTC | Comprehensive build + 12 product profiles + dependency audit |
| **EoSim Sanity** | 4:00 AM UTC daily | EoSim install (3 OS × 3 Python) + 7-platform simulation |
| **Simulation Test** | 3:00 AM UTC daily | QEMU/EoSim platform simulation across 11 board types |
| **Release** | Tag `v*.*.*` | Validate → cross-compile → GitHub Release with artifacts |

### Site Structure

```
embeddedos-org.github.io/
├── index.html              Homepage — ecosystem overview, hardware, architecture
├── getting-started.html    Quick start guide
├── flow.html               Platform flow diagram
├── hardware-lab.html       Interactive hardware lab
├── kids.html               Educational resources
├── docs/
│   ├── index.html          Documentation hub
│   ├── eos.html            EoS Core docs
│   ├── eboot.html          eBoot docs
│   ├── ebuild.html         eBuild docs
│   ├── eipc.html           EIPC docs
│   ├── eai.html            EAI docs
│   ├── eni.html            ENI docs
│   ├── eosuite.html        eApps docs
│   ├── eosim.html          EoSim docs
│   ├── eostudio.html       EoStudio docs
│   ├── edb.html            eDB docs
│   ├── ebrowser.html       eBrowser docs
│   ├── eoffice.html        eOffice docs
│   └── embeddedos-ecosystem-guide.md  Long-form ecosystem guide
├── eApps/
│   └── index.html          App Store frontend
├── style.css               Design system
└── tests/                  Playwright responsive tests
```

## Security

### Security Headers

The `_headers` file configures HTTP security headers for the GitHub Pages site:

- **X-Frame-Options: DENY** — Prevents clickjacking by blocking iframe embedding
- **X-Content-Type-Options: nosniff** — Prevents MIME-type sniffing attacks
- **X-XSS-Protection: 1; mode=block** — Enables browser XSS filtering
- **Referrer-Policy: strict-origin-when-cross-origin** — Limits referrer information leakage
- **Permissions-Policy** — Disables camera, microphone, and geolocation APIs
- **Content-Security-Policy** — Restricts resource loading to trusted origins

### Internal URL Policy

Documentation pages use `localhost` and `192.168.x.x` addresses in code examples (eDB API examples, eIPC connection strings, ebuild OTA commands, hardware lab SSH). These are **example/placeholder addresses only** and do not represent real infrastructure. Contributors should:

- Never include real internal hostnames or IP addresses in documentation
- Use `localhost`, `192.168.x.x`, or `example.com` for all code examples
- Review PRs for accidental inclusion of internal URLs before merging

### Reporting Vulnerabilities

If you discover a security vulnerability in any EmbeddedOS component, please report it responsibly by opening a private security advisory on the affected repository. Do not file public issues for security vulnerabilities.

## Standards Compliance

ISO/IEC/IEEE 15288:2023 · ISO/IEC 12207 · ISO/IEC 25000 · ISO/IEC 27001 · IEC 61508 · ISO 26262 · DO-178C · FIPS 140-3 · POSIX · WCAG 2.1 · NTIA SBOM · SPDX · CycloneDX · OpenChain

## License

MIT License — see [LICENSE](LICENSE) for details.

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Related Meta-Repos

These are **not** part of the canonical 13 product repos. They are
organisation-level meta-repos that compose, route to, or describe the
canonical roster.

| Repo | Role |
|---|---|
| [.github](https://github.com/embeddedos-org/.github) | Org-wide configuration: org-profile page (rendered at <https://github.com/embeddedos-org>), default `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, issue/PR templates, canon validator. |
| [embeddedos-org.github.io](https://github.com/embeddedos-org/embeddedos-org.github.io) | This site — developer portal, books, docs hub, downloads, stacks. |
| [eFab](https://github.com/embeddedos-org/eFab) | **Stack fabricator** — manifest-only meta-repo that pins versions, fetches sources, and runs end-to-end smoke tests for opinionated bundles of canonical products. v0.1.0 ships the `eai-edge` profile (ENI + EIPC + eAI). See [/stacks/](https://embeddedos-org.github.io/stacks/). |
