# EoS — Embedded Operating System

**Website**: [embeddedos-org.github.io](https://embeddedos-org.github.io)

## v0.1.0 Release

All 10 repositories at v0.1.0, 1 commit each.

### Ecosystem

| Repo | Description | Version |
|---|---|---|
| [eos](https://github.com/embeddedos-org/eos) | Core OS — HAL (33 peripherals), RTOS kernel, services, GDB stub, core dump, service manager, loadable drivers, device tree parser | v0.1.0 |
| [eboot](https://github.com/embeddedos-org/eboot) | Bootloader — 24 board ports, A/B update, secure boot, crypto, multicore boot | v0.1.0 |
| [ebuild](https://github.com/embeddedos-org/ebuild) | Build system — SDK generator (14 targets), eBoot board generator, deliverable packager, gated release | v0.1.0 |
| [eipc](https://github.com/embeddedos-org/eipc) | Secure IPC — Go + C SDK, HMAC, replay protection, TCP/Unix/SHM transports | v0.1.0 |
| [eai](https://github.com/embeddedos-org/eai) | AI layer — llama.cpp, 12 LLM models, agent loop, Ebot server, adaptive learning | v0.1.0 |
| [eni](https://github.com/embeddedos-org/eni) | Neural interface — BCI, Neuralink adapter, assistive input, DSP, neural net | v0.1.0 |
| [eApps](https://github.com/embeddedos-org/eApps) | Cross-platform apps — 38 C + LVGL apps (productivity, media, games, connectivity) | v0.1.0 |
| [eosim](https://github.com/embeddedos-org/eosim) | Simulator — 41 platforms, 12 architectures, EoSim native engine | v0.1.0 |
| [EoStudio](https://github.com/embeddedos-org/EoStudio) | Design suite — 10 editors (3D, CAD, image, game, UI, UML, simulation, database), LLM | v0.1.0 |

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
# Generate SDK for target
ebuild sdk --target raspi4

# Source environment
source build/eos-sdk-raspi4/environment-setup

# Build
cmake -B build -DCMAKE_TOOLCHAIN_FILE=$CMAKE_TOOLCHAIN_FILE
cmake --build build

# Deploy
scp build/app pi@192.168.1.100:~/

# Build eApps (38 cross-platform apps)
cd eApps && cmake -B build -DEAPPS_PORT=sdl2 && cmake --build build
```

### CI/CD

Every repository runs automated CI/CD via GitHub Actions:

| Workflow | Schedule | Coverage |
|----------|----------|----------|
| **CI** | Every push/PR | Build + test on Linux × Windows × macOS |
| **Nightly** | 2:00 AM UTC daily | Full regression suite + cross-compile |
| **Weekly** | Monday 6:00 AM UTC | Comprehensive build + 12 product profiles + dependency audit |
| **EoSim Sanity** | 4:00 AM UTC daily | EoSim install (3 OS × 3 Python) + 7-platform simulation + nested guest boot |
| **Simulation Test** | 3:00 AM UTC daily | QEMU/EoSim platform simulation across 11 board types |
| **Release** | Tag `v*.*.*` | Validate → cross-compile → GitHub Release with artifacts |

- Gated release — all repos must pass before release
- 100+ CI jobs across all repos per push
- 11 QEMU board types, 6+ architectures
- Cross-repo dispatch — change in any core repo validates all dependents

## Standards Compliance

This project is part of the EoS ecosystem and aligns with international standards including ISO/IEC/IEEE 15288:2023, ISO/IEC 12207, ISO/IEC/IEEE 42010, ISO/IEC 25000, ISO/IEC 25010, ISO/IEC 27001, ISO/IEC 15408, IEC 61508, ISO 26262, DO-178C, FIPS 140-3, POSIX (IEEE 1003), WCAG 2.1, and more. See the [EoS Compliance Documentation](https://github.com/embeddedos-org/.github/tree/master/docs/compliance) for full details including NTIA SBOM, SPDX, CycloneDX, and OpenChain compliance.

## License

MIT License — see [LICENSE](LICENSE) for details.
