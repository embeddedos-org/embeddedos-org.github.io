# EoS — Embedded Operating System Developer Portal

**Website**: [embeddedos-org.github.io](https://embeddedos-org.github.io)

**Foundation**: [embeddedos-org.github.io](https://embeddedos-org.github.io)

**App Store**: [embeddedos-org.github.io/eApps](https://embeddedos-org.github.io/eApps/)

## v0.1.0 Release

All repositories at v0.1.0 — a complete embedded AI systems stack.

### Ecosystem (14 Components)

| Repo | Description | Language | Version |
|---|---|---|---|
| [eos](https://github.com/embeddedos-org/eos) | Core OS — HAL (33 peripherals), RTOS kernel, multicore SMP/AMP, services, GDB stub, core dump, loadable drivers, device tree parser | C11 | v0.1.0 |
| [eboot](https://github.com/embeddedos-org/eboot) | Bootloader — 24 board ports, A/B update, secure boot, crypto, multicore boot, UEFI device table | C11 | v0.1.0 |
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
| [eServiceApps](https://github.com/embeddedos-org/eServiceApps) | Mobile apps — eSocial, eRide, eTravel, eTrack, eWallet (Flutter) | Dart | v0.1.0 |
| [eos-platform](https://github.com/embeddedos-org/eos-platform) | Platform layer — Desktop, TV, Laptop, Tablet, Kiosk profiles on EoS | C | v0.1.0 |

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
│   ├── ebowser.html        eBowser docs
│   ├── eoffice.html        eOffice docs
│   └── eserviceapps.html   eServiceApps docs
├── eApps/
│   └── index.html          App Store frontend
├── style.css               Design system
└── tests/                  Playwright responsive tests
```

## Standards Compliance

ISO/IEC/IEEE 15288:2023 · ISO/IEC 12207 · ISO/IEC 25000 · ISO/IEC 27001 · IEC 61508 · ISO 26262 · DO-178C · FIPS 140-3 · POSIX · WCAG 2.1 · NTIA SBOM · SPDX · CycloneDX · OpenChain

## License

MIT License — see [LICENSE](LICENSE) for details.
