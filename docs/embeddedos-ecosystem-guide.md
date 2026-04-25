---
title: "The EmbeddedOS Ecosystem — Complete Product Guide"
author: "Srikanth Patchava & EmbeddedOS Contributors"
date: "April 2026"
version: "1.0.0"
license: "MIT"
---

# The EmbeddedOS Ecosystem — Complete Product Guide

**By Srikanth Patchava & EmbeddedOS Contributors**

**First Edition — April 2026**

---

> *"From silicon to space — one ecosystem, infinite possibilities."*

---

**Copyright 2026 EmbeddedOS Contributors. MIT License.**

---

## Table of Contents

- [Preface](#preface)
- **Part I: Platform Foundation**
  - [Chapter 1: eos — The Embedded Operating System](#chapter-1-eos--the-embedded-operating-system)
  - [Chapter 2: eBoot — Secure Bootloader](#chapter-2-eboot--secure-bootloader)
  - [Chapter 3: ebuild — Build System](#chapter-3-ebuild--build-system)
  - [Chapter 4: eIPC — Inter-Process Communication](#chapter-4-eipc--inter-process-communication)
  - [Chapter 5: eDB — Embedded Database](#chapter-5-edb--embedded-database)
- **Part II: Application Layer**
  - [Chapter 6: eBrowser — Embedded Web Browser](#chapter-6-ebrowser--embedded-web-browser)
  - [Chapter 7: eOffice — Office Productivity Suite](#chapter-7-eoffice--office-productivity-suite)
  - [Chapter 8: eVera — AI Virtual Assistant](#chapter-8-evera--ai-virtual-assistant)
  - [Chapter 9: eApps — Mobile App Platform](#chapter-9-eapps--mobile-app-platform)
  - [Chapter 10: EoStudio — Development Environment](#chapter-10-eostudio--development-environment)
- **Part III: Intelligence Layer**
  - [Chapter 11: eAI — AI/ML Inference Engine](#chapter-11-eai--aiml-inference-engine)
  - [Chapter 12: eNI — Neural Interface](#chapter-12-eni--neural-interface)
  - [Chapter 13: eStocks — Algorithmic Trading](#chapter-13-estocks--algorithmic-trading)
- **Part IV: Hardware Products**
  - [Chapter 14: eRadar360 — Automotive Radar](#chapter-14-eradar360--automotive-radar)
  - [Chapter 15: eHealth365 — Health Monitoring](#chapter-15-ehealth365--health-monitoring)
  - [Chapter 16: ePAM — Personal Air Mobility](#chapter-16-epam--personal-air-mobility)
- **Part V: Development and Operations**
  - [Chapter 17: EoSim — Simulation Environment](#chapter-17-eosim--simulation-environment)
  - [Chapter 18: Cross-Product Integration](#chapter-18-cross-product-integration)
- **Part VI: Organization**
  - [Chapter 19: Governance and Contribution Model](#chapter-19-governance-and-contribution-model)
  - [Chapter 20: embeddedos-org.github.io — The Documentation Hub](#chapter-20-embeddedos-orggithubio--the-documentation-hub)
- [Appendix A: Repository Quick Reference](#appendix-a-repository-quick-reference)
- [Appendix B: Technology Stack Summary](#appendix-b-technology-stack-summary)
- [Appendix C: Getting Started Guide](#appendix-c-getting-started-guide)
- [Glossary](#glossary)

---

## Preface

### The EmbeddedOS Vision

EmbeddedOS began with a simple but audacious goal: create a fully integrated ecosystem
that spans from bare-metal firmware to cloud-connected applications, from wearable health
sensors to suborbital spacecraft. What started as a real-time operating system kernel has
grown into a 16-repository organization that covers the entire stack of modern embedded
and intelligent systems.

This guide serves as the **omnibus reference** for the entire EmbeddedOS ecosystem. Whether
you are a firmware engineer working on device drivers, a web developer building office
productivity tools, a data scientist training on-device ML models, or a hardware designer
laying out PCBs -- this book is your comprehensive companion.

### How the Products Connect

The EmbeddedOS ecosystem is organized in **concentric layers**:

```
+------------------------------------------------------------------+
|                    HARDWARE PRODUCTS                              |
|         eRadar360 - eHealth365 - ePAM Vehicles                   |
|    +----------------------------------------------------------+  |
|    |              INTELLIGENCE LAYER                           |  |
|    |         eAI - eNI - eStocks Trading                      |  |
|    |    +--------------------------------------------------+  |  |
|    |    |          APPLICATION LAYER                        |  |  |
|    |    |   eBrowser - eOffice - eVera - eApps              |  |  |
|    |    |    +------------------------------------------+   |  |  |
|    |    |    |    PLATFORM FOUNDATION                   |   |  |  |
|    |    |    |  eos - eBoot - ebuild                    |   |  |  |
|    |    |    |  eIPC - eDB                              |   |  |  |
|    |    |    +------------------------------------------+   |  |  |
|    |    +--------------------------------------------------+  |  |
|    +----------------------------------------------------------+  |
|                                                                  |
|    TOOLING: EoStudio - EoSim - ebuild - Documentation Hub        |
+------------------------------------------------------------------+
```

**Key integration points:**

- **eos** provides the RTOS kernel that runs on all hardware products
- **eBoot** secures the boot chain for eRadar360, eHealth365, and ePAM devices
- **eAI** provides on-device inference used by eHealth365 health scoring, eRadar360
  object detection, ePAM autonomous navigation, and eVera language understanding
- **eIPC** connects processes across eos, eBrowser, eOffice, and eVera
- **eDB** stores data for eOffice documents, eVera memory, and eStocks market data
- **ebuild** compiles and packages every C/C++ component, including KiCad hardware
  design analysis for eHardware-Designs-Products
- **EoSim** simulates the full hardware-software stack before physical deployment
- **EoStudio** provides the IDE for developing across all repositories

### Who This Book Is For

| Audience | Start Here |
|----------|-----------|
| Firmware engineers | Part I (eos, eBoot) |
| Application developers | Part II (eBrowser, eOffice, eVera) |
| AI/ML engineers | Part III (eAI, eNI) |
| Hardware designers | Part IV (eRadar360, eHealth365, ePAM) |
| DevOps / Build engineers | Part V (EoSim, ebuild) |
| Contributors | Part VI (Governance) |

---

# Part I: Platform Foundation

---

## Chapter 1: eos -- The Embedded Operating System

### Overview

**Repository:** `embeddedos-org/eos`
**Language:** C/C++
**License:** MIT
**Status:** Active Development

eos is the core real-time operating system that powers the entire EmbeddedOS hardware
ecosystem. It provides a preemptive RTOS kernel, hardware abstraction layer (HAL),
device drivers, and system services designed for deterministic, low-latency operation
on resource-constrained embedded devices.

### Key Features

- **Preemptive RTOS Kernel** -- Priority-based preemptive scheduling with configurable
  tick rate (1 kHz default), supporting up to 256 priority levels
- **Hardware Abstraction Layer (HAL)** -- Uniform API across ARM Cortex-M, Cortex-A,
  RISC-V, and x86 architectures
- **Device Driver Framework** -- Modular driver model for GPIO, UART, SPI, I2C, ADC,
  DAC, PWM, CAN, Ethernet, USB, and custom peripherals
- **Memory Management** -- Static and dynamic allocation with memory pools, heap
  management with fragmentation protection, and MPU support
- **Power Management** -- Tickless idle, deep sleep modes, peripheral clock gating,
  and dynamic voltage/frequency scaling (DVFS)
- **File System Support** -- FAT32, LittleFS, and custom flash-optimized file systems
- **Networking Stack** -- lwIP integration with TCP/UDP/IPv4/IPv6, TLS 1.3 via mbedTLS
- **POSIX Compatibility Layer** -- Subset of POSIX API for portable application code

### Architecture

```
+-------------------------------------------------------+
|                   User Applications                    |
+-------------------------------------------------------+
|  POSIX Layer  |  Networking  |  File System  |  Shell  |
+-------------------------------------------------------+
|                   System Services                      |
|    Timers | Events | Queues | Mutexes | Semaphores     |
+-------------------------------------------------------+
|                    RTOS Kernel                          |
|  Scheduler | Context Switch | Interrupt Mgmt | Memory  |
+-------------------------------------------------------+
|             Hardware Abstraction Layer (HAL)            |
|   GPIO | UART | SPI | I2C | ADC | CAN | USB | ETH     |
+-------------------------------------------------------+
|              Board Support Packages (BSP)              |
|  STM32F4xx | STM32H7xx | nRF52840 | ESP32 | RISC-V   |
+-------------------------------------------------------+
```

### Getting Started

```c
#include <eos/kernel.h>
#include <eos/hal/gpio.h>
#include <eos/task.h>

/* Blink LED task */
void blink_task(void *params) {
    gpio_pin_t led = GPIO_PIN(GPIOB, 7);
    gpio_init(led, GPIO_MODE_OUTPUT);

    while (1) {
        gpio_toggle(led);
        eos_task_delay_ms(500);
    }
}

int main(void) {
    eos_kernel_init();

    eos_task_create("blink", blink_task, NULL,
                    EOS_TASK_PRIORITY_NORMAL, 512);

    eos_kernel_start();  /* Never returns */
    return 0;
}
```

### API Highlights

#### Kernel API

| Function | Description |
|----------|-------------|
| `eos_kernel_init()` | Initialize kernel and HAL |
| `eos_kernel_start()` | Start scheduler (never returns) |
| `eos_kernel_get_tick()` | Get current system tick count |
| `eos_kernel_enter_critical()` | Disable interrupts, enter critical section |
| `eos_kernel_exit_critical()` | Re-enable interrupts, exit critical section |

#### Task API

| Function | Description |
|----------|-------------|
| `eos_task_create()` | Create a new task with priority and stack size |
| `eos_task_delete()` | Delete a task |
| `eos_task_delay_ms()` | Delay task for specified milliseconds |
| `eos_task_suspend()` | Suspend a task |
| `eos_task_resume()` | Resume a suspended task |
| `eos_task_yield()` | Yield CPU to next ready task |

#### HAL GPIO API

| Function | Description |
|----------|-------------|
| `gpio_init()` | Initialize GPIO pin with mode |
| `gpio_write()` | Write digital value to pin |
| `gpio_read()` | Read digital value from pin |
| `gpio_toggle()` | Toggle pin state |
| `gpio_set_interrupt()` | Configure pin interrupt with callback |

### Supported Platforms

| Platform | Architecture | Status |
|----------|-------------|--------|
| STM32F4xx | ARM Cortex-M4 | Production |
| STM32H7xx | ARM Cortex-M7 | Production |
| nRF52840 | ARM Cortex-M4 | Production |
| ESP32-S3 | Xtensa LX7 | Beta |
| RISC-V (SiFive) | RV32IMAC | Beta |
| Raspberry Pi Pico | ARM Cortex-M0+ | Production |
| i.MX RT1060 | ARM Cortex-M7 | Production |

---

## Chapter 2: eBoot -- Secure Bootloader

### Overview

**Repository:** `embeddedos-org/eBoot`
**Language:** C/Assembly
**License:** MIT
**Status:** Active Development

eBoot is a secure bootloader designed to establish a hardware root of trust for all
EmbeddedOS-powered devices. It implements verified boot chains, firmware update
mechanisms, and board-specific port layers for diverse hardware platforms.

### Key Features

- **Secure Boot Chain** -- Multi-stage verified boot with RSA-2048/Ed25519 signature
  verification at each stage
- **Firmware Update (FOTA)** -- Over-the-air and USB firmware updates with rollback
  protection via A/B partition scheme
- **Hardware Root of Trust** -- Integration with hardware security modules (HSM),
  TPM 2.0, and ARM TrustZone
- **Board-Specific Ports** -- Modular port architecture supporting STM32, nRF, ESP32,
  RISC-V, and custom SoCs
- **Minimal Footprint** -- Stage 1 bootloader fits in 8 KB; full bootloader under 64 KB
- **Anti-Rollback Protection** -- Monotonic version counters stored in OTP fuses
- **Recovery Mode** -- Failsafe recovery via UART/USB when primary firmware is corrupted
- **Encryption Support** -- AES-256-GCM firmware image encryption at rest

### Architecture

```
+--------------------------------------------------+
|              Power On / Reset                     |
+--------------------------------------------------+
               |
               v
+--------------------------------------------------+
|  Stage 0: ROM Bootloader (SoC-specific)          |
|  - Initialize clocks, basic SRAM                 |
|  - Verify Stage 1 signature (if HW supported)    |
+--------------------------------------------------+
               |
               v
+--------------------------------------------------+
|  Stage 1: eBoot Primary (8 KB)                   |
|  - Initialize flash controller                   |
|  - Verify Stage 2 signature (Ed25519)            |
|  - Select active partition (A/B)                 |
+--------------------------------------------------+
               |
               v
+--------------------------------------------------+
|  Stage 2: eBoot Secondary (up to 56 KB)          |
|  - Full hardware initialization                  |
|  - Verify eos kernel image                       |
|  - Apply firmware updates if pending             |
|  - Initialize MPU/TrustZone                      |
+--------------------------------------------------+
               |
               v
+--------------------------------------------------+
|  eos Kernel Boot                                 |
|  - Jump to kernel entry point                    |
|  - Pass boot parameters and hardware info        |
+--------------------------------------------------+
```

### Getting Started

```c
/* eBoot board port configuration -- board_config.h */
#include <eboot/config.h>

#define EBOOT_BOARD_NAME        "eHealth365_SmartRing"
#define EBOOT_FLASH_BASE        0x08000000
#define EBOOT_FLASH_SIZE        (2 * 1024 * 1024)  /* 2 MB */
#define EBOOT_PARTITION_A       0x08010000
#define EBOOT_PARTITION_B       0x08110000
#define EBOOT_PARTITION_SIZE    (1024 * 1024)       /* 1 MB each */

#define EBOOT_SIGN_ALGO         EBOOT_SIGN_ED25519
#define EBOOT_ENCRYPT_ALGO      EBOOT_ENCRYPT_AES256_GCM
#define EBOOT_ANTI_ROLLBACK     1
#define EBOOT_RECOVERY_UART     USART1
#define EBOOT_RECOVERY_BAUD     115200
```

### API Highlights

| Function | Description |
|----------|-------------|
| `eboot_verify_image()` | Verify firmware image signature |
| `eboot_install_update()` | Install firmware update to inactive partition |
| `eboot_get_active_partition()` | Get currently active boot partition |
| `eboot_mark_valid()` | Mark current firmware as valid (confirm update) |
| `eboot_rollback()` | Roll back to previous firmware version |
| `eboot_enter_recovery()` | Enter UART/USB recovery mode |
| `eboot_get_version()` | Get bootloader version info |

---

## Chapter 3: ebuild -- Build System

### Overview

**Repository:** `embeddedos-org/ebuild`
**Language:** Python, CMake, Make
**License:** MIT
**Status:** Active Development

ebuild is the unified build system for the EmbeddedOS ecosystem. It orchestrates
compilation of C/C++ firmware, packaging of web applications, and analysis of KiCad
hardware designs -- all from a single command-line interface.

### Key Features

- **Multi-Target Build** -- Build firmware for multiple architectures and boards in
  parallel from a single configuration
- **KiCad Hardware Analyzer** -- Parse KiCad schematics and PCB layouts to extract BOM,
  netlist, design rule checks, and cross-reference with firmware pin assignments
- **Dependency Management** -- Automatic resolution of inter-repository dependencies
  with version pinning and lockfiles
- **Toolchain Management** -- Auto-download and configure ARM GCC, RISC-V GCC, Clang,
  and vendor-specific toolchains
- **Reproducible Builds** -- Deterministic builds with SHA-256 build artifacts and
  SBOM generation
- **CI/CD Integration** -- GitHub Actions, GitLab CI, and Jenkins pipeline generators
- **Flash and Debug** -- Integrated flashing via OpenOCD, J-Link, and vendor tools

### Architecture

```
+------------------------------------------------------+
|                ebuild CLI (Python)                    |
|  ebuild config | build | flash | test | analyze      |
+------------------------------------------------------+
|              Build Configuration Engine               |
|   ebuild.yaml | board configs | target definitions    |
+----------+-----------+-----------+-------------------+
| CMake    | Webpack/  | KiCad     | Toolchain         |
| Backend  | Vite      | Analyzer  | Manager           |
| (C/C++)  | (Web)     | (HW)     |                    |
+----------+-----------+-----------+-------------------+
|           Artifact Manager and Cache                  |
|   Build cache | SBOM | Signing | Distribution         |
+------------------------------------------------------+
```

### Getting Started

```yaml
# ebuild.yaml -- project configuration
project:
  name: eHealth365_firmware
  version: 2.1.0
  license: MIT

targets:
  smart_ring:
    board: nrf52840_custom
    toolchain: arm-none-eabi-gcc-13
    kernel: eos@latest
    bootloader: eBoot@latest
    features:
      - ble5
      - sensor_hub
      - low_power

  smart_patch:
    board: stm32h743_custom
    toolchain: arm-none-eabi-gcc-13
    kernel: eos@latest
    bootloader: eBoot@latest
    features:
      - cgm_sensor
      - sweat_analysis
      - ble5
      - nfc

dependencies:
  eAI: ^1.2.0
  eIPC: ^0.8.0
  eDB: ^1.0.0
```

```bash
# Build all targets
ebuild build --all --parallel

# Build specific target with debug symbols
ebuild build smart_ring --debug

# Analyze KiCad hardware design
ebuild analyze --kicad smart_ring

# Flash firmware
ebuild flash smart_ring --probe jlink
```

### API Highlights -- KiCad Analyzer

| Command | Description |
|---------|-------------|
| `ebuild analyze --bom` | Generate Bill of Materials from schematic |
| `ebuild analyze --netlist` | Extract netlist and verify connectivity |
| `ebuild analyze --drc` | Run design rule checks on PCB layout |
| `ebuild analyze --pin-map` | Cross-reference schematic pins with firmware HAL |
| `ebuild analyze --power` | Estimate power consumption from component specs |
| `ebuild analyze --thermal` | Basic thermal analysis from PCB copper area |

---

## Chapter 4: eIPC -- Inter-Process Communication

### Overview

**Repository:** `embeddedos-org/eIPC`
**Language:** C/C++
**License:** MIT
**Status:** Active Development

eIPC is a high-performance inter-process communication library designed for
embedded systems. It provides zero-copy message passing, shared memory regions,
publish-subscribe patterns, and remote procedure calls (RPC) -- all with minimal
overhead suitable for real-time applications.

### Key Features

- **Zero-Copy Message Passing** -- Lock-free ring buffers for inter-task communication
  with zero memory copies on shared-memory architectures
- **Publish-Subscribe** -- Topic-based pub/sub with QoS levels (best-effort,
  reliable, transactional)
- **Remote Procedure Call (RPC)** -- Synchronous and asynchronous RPC with automatic
  serialization via Protocol Buffers or MessagePack
- **Shared Memory** -- Named shared memory regions with access control and
  reader-writer synchronization
- **Cross-Platform** -- Works on eos native, Linux, macOS, and Windows
- **Transport Abstraction** -- Pluggable transports: in-process, inter-process
  (Unix sockets/pipes), network (TCP/UDP), and serial (UART/SPI)
- **Discovery Service** -- Automatic service discovery for dynamic system topologies

### Architecture

```
+-----------------------------------------------------+
|              Application Layer                       |
|   Publisher | Subscriber | RPC Client | RPC Server   |
+-----------------------------------------------------+
|              eIPC Core Library                       |
|  Serialization | Routing | QoS | Discovery | Auth   |
+-------------+------------+------------+-------------+
| In-Process  | IPC        | Network    | Serial      |
| (Ring Buf)  | (Sockets)  | (TCP/UDP)  | (UART/SPI)  |
+-------------+------------+------------+-------------+
```

### Getting Started

```c
#include <eipc/eipc.h>
#include <eipc/pubsub.h>

void sensor_publisher(void) {
    eipc_node_t *node = eipc_node_create("sensor_hub");
    eipc_publisher_t *pub = eipc_advertise(node, "sensor/heartrate",
                                            EIPC_MSG_FLOAT32, EIPC_QOS_RELIABLE);
    while (1) {
        float hr = read_heart_rate_sensor();
        eipc_publish(pub, &hr, sizeof(hr));
        eos_task_delay_ms(100);
    }
}

void health_monitor(void) {
    eipc_node_t *node = eipc_node_create("health_monitor");
    eipc_subscriber_t *sub = eipc_subscribe(node, "sensor/heartrate",
                                             EIPC_MSG_FLOAT32, EIPC_QOS_RELIABLE);
    float hr;
    while (1) {
        if (eipc_receive(sub, &hr, sizeof(hr), EIPC_WAIT_FOREVER) == EIPC_OK) {
            process_heart_rate(hr);
        }
    }
}
```

### API Highlights

| Function | Description |
|----------|-------------|
| `eipc_node_create()` | Create a communication node |
| `eipc_advertise()` | Create a publisher on a topic |
| `eipc_subscribe()` | Subscribe to a topic |
| `eipc_publish()` | Publish a message |
| `eipc_receive()` | Receive a message (blocking/non-blocking) |
| `eipc_rpc_register()` | Register an RPC service handler |
| `eipc_rpc_call()` | Call a remote procedure |
| `eipc_shm_create()` | Create a named shared memory region |
| `eipc_shm_attach()` | Attach to an existing shared memory region |

---

## Chapter 5: eDB -- Embedded Database

### Overview

**Repository:** `embeddedos-org/eDB`
**Language:** C
**License:** MIT
**Status:** Active Development

eDB is a lightweight, embedded database engine optimized for flash-based storage
on resource-constrained devices. It provides key-value storage, document storage
with JSON-like queries, and time-series data management -- all with ACID guarantees
and wear-leveling for flash memory.

### Key Features

- **Key-Value Store** -- O(log n) lookups with B+ tree indexing on flash
- **Document Store** -- BSON document storage with query support for nested fields
- **Time-Series Engine** -- Optimized append-only storage for sensor data with
  automatic downsampling and retention policies
- **ACID Transactions** -- Write-ahead logging (WAL) with crash recovery
- **Flash Wear Leveling** -- Intelligent block allocation to extend flash lifetime
- **Tiny Footprint** -- Core engine under 32 KB ROM, 4 KB minimum RAM
- **Encryption at Rest** -- AES-256 transparent encryption for stored data
- **Replication** -- Optional master-replica replication over eIPC for redundancy

### Architecture

```
+-------------------------------------------------+
|             Application Interface                |
|   KV API | Document API | Time-Series API        |
+-------------------------------------------------+
|               Query Engine                       |
|   Parser | Planner | Executor | Aggregation      |
+-------------------------------------------------+
|              Storage Engine                      |
|   B+ Tree | LSM Tree | Append Log | WAL         |
+-------------------------------------------------+
|            Flash Translation Layer               |
|   Wear Leveling | Bad Block Mgmt | Compaction    |
+-------------------------------------------------+
|        Hardware: NOR/NAND Flash, eMMC, SD        |
+-------------------------------------------------+
```

### Getting Started

```c
#include <edb/edb.h>

int main(void) {
    edb_t *db;
    edb_config_t config = {
        .path = "/flash/health_data",
        .max_size = 1024 * 1024,
        .encryption = EDB_ENCRYPT_AES256,
        .wear_leveling = true
    };
    edb_open(&db, &config);

    edb_kv_put(db, "user.name", "Patient_001", 11);

    edb_ts_t *ts;
    edb_ts_create(db, &ts, "heartrate", EDB_TS_FLOAT32, EDB_TS_DOWNSAMPLE_AVG);
    float hr_sample = 72.5f;
    edb_ts_append(ts, eos_kernel_get_tick(), &hr_sample);

    edb_close(db);
    return 0;
}
```

### API Highlights

| Function | Description |
|----------|-------------|
| `edb_open()` / `edb_close()` | Open/close database |
| `edb_kv_put()` / `edb_kv_get()` | Key-value store/retrieve |
| `edb_kv_delete()` | Delete a key |
| `edb_ts_create()` | Create time-series collection |
| `edb_ts_append()` | Append time-series data point |
| `edb_ts_query()` | Query time-series with time range and aggregation |
| `edb_doc_insert()` | Insert JSON document |
| `edb_doc_find()` | Query documents with filter expression |
| `edb_txn_begin()` / `edb_txn_commit()` | Transaction boundaries |
| `edb_compact()` | Manual compaction and garbage collection |

---

# Part II: Application Layer

---

## Chapter 6: eBrowser -- Embedded Web Browser

### Overview

**Repository:** `embeddedos-org/eBrowser`
**Language:** C/C++
**Build System:** CMake
**UI Frameworks:** SDL2, LVGL v9.2
**License:** MIT
**Status:** Active Development

eBrowser is a lightweight web browser purpose-built for embedded and IoT devices.
Unlike desktop browsers that require gigabytes of RAM, eBrowser is designed to render
modern web content on devices with as little as 16 MB of RAM, making it suitable for
kiosks, automotive infotainment, smart home panels, industrial HMIs, and embedded
dashboard displays.

### Key Features

- **HTML5/CSS3 Rendering** -- Core HTML5 elements, CSS3 flexbox/grid layout
- **JavaScript Engine** -- Lightweight JS interpreter with ES6+ support
- **SDL2 Rendering Backend** -- Hardware-accelerated rendering via SDL2
- **LVGL v9.2 Integration** -- Native LVGL widget rendering for embedded UI
- **Network Stack** -- HTTP/1.1 and HTTPS with TLS 1.3, connection pooling, caching
- **Input Handling** -- Touch, mouse, keyboard, rotary encoder, gesture recognition
- **Platform Abstraction Layer** -- Linux FB, X11, Wayland, SDL2, eos framebuffer
- **7 Test Suites, 130+ Tests** -- Comprehensive test coverage

### Architecture

```
+--------------------------------------------------------------+
|                    User Interface Layer                        |
|   Tab Manager | Address Bar | Bookmarks | Settings | DevTools |
+--------------------------------------------------------------+
|                     Core Engine                               |
|  +---------+ +---------+ +---------+ +-------------+         |
|  |  HTML   | |  CSS    | |  Layout | |  JavaScript |         |
|  |  Parser | |  Parser | |  Engine | |  Engine     |         |
|  |  DOM    | |  CSSOM  | | Flex/   | |  (ES6+)     |         |
|  |         | |         | | Grid    | |             |         |
|  +---------+ +---------+ +---------+ +-------------+         |
+--------------------------------------------------------------+
|                  Rendering Backend                            |
|     SDL2 Renderer | LVGL v9.2 | Canvas | Font Engine         |
+--------------------------------------------------------------+
|                    Network Stack                              |
|     HTTP Client | TLS 1.3 | DNS | Cache | Cookie Manager     |
+--------------------------------------------------------------+
|                     Input Layer                               |
|     Touch | Mouse | Keyboard | Rotary Encoder | Gestures     |
+--------------------------------------------------------------+
|              Platform Abstraction Layer (PAL)                 |
|   Linux FB | X11 | Wayland | SDL2 Window | eos Framebuffer   |
+--------------------------------------------------------------+
```

### Getting Started

```bash
git clone https://github.com/embeddedos-org/eBrowser.git
cd eBrowser
mkdir build && cd build
cmake .. -DEBROWSER_BACKEND=SDL2 \
         -DEBROWSER_ENABLE_JS=ON \
         -DEBROWSER_ENABLE_LVGL=ON \
         -DCMAKE_BUILD_TYPE=Debug
make -j$(nproc)
./ebrowser --url "https://example.com"
ctest --output-on-failure
```

### Embedding API (C++)

```cpp
#include <ebrowser/engine.h>
#include <ebrowser/view.h>

ebrowser::Engine engine;
engine.init({
    .backend = ebrowser::Backend::SDL2,
    .width = 800,
    .height = 480,
    .enable_js = true,
    .cache_size_mb = 8
});

auto view = engine.create_view();
view->navigate("https://dashboard.local");
view->on_load([](ebrowser::View& v) {
    printf("Page loaded: %s\n", v.get_title().c_str());
});

engine.run();
```

### Test Coverage Summary

| Test Suite | Tests | Coverage Area |
|-----------|-------|---------------|
| HTML Parser | 22 | Tag parsing, DOM construction, error recovery |
| CSS Parser | 18 | Selector matching, cascade, specificity |
| Layout Engine | 25 | Box model, flexbox, grid, text layout |
| JavaScript | 20 | ES6+ features, DOM manipulation, events |
| Network | 15 | HTTP requests, TLS, caching, cookies |
| Input | 12 | Touch, keyboard, gestures, focus management |
| Integration | 18+ | End-to-end page rendering, navigation |
| **Total** | **130+** | |

---

## Chapter 7: eOffice -- Office Productivity Suite

### Overview

**Repository:** `embeddedos-org/eOffice`
**Language:** TypeScript, JavaScript
**Frontend:** React 18, Vite
**Backend:** Express.js, Node.js
**Desktop:** Electron
**License:** MIT
**Status:** Active Development

eOffice is a complete, AI-powered office productivity suite comprising 12 integrated
applications enhanced by eBot, an AI assistant with 33+ intelligent actions.

### The 12 Applications

| # | App | Description |
|---|-----|-------------|
| 1 | **eDocs** | Rich text document editor with collaborative editing |
| 2 | **eSheets** | Spreadsheet with formulas, charts, and pivot tables |
| 3 | **eSlides** | Presentation creator with templates and animations |
| 4 | **eNotes** | Note-taking with markdown, tags, and notebooks |
| 5 | **eMail** | Email client with smart inbox and filtering |
| 6 | **eDB** | Database management interface (visual SQL/NoSQL) |
| 7 | **eDrive** | Cloud file storage with sharing and versioning |
| 8 | **eConnect** | Video conferencing and team messaging |
| 9 | **eForms** | Form builder with logic, validation, and responses |
| 10 | **eSway** | Interactive content and newsletter creator |
| 11 | **ePlanner** | Project management with Kanban, Gantt, and calendars |
| 12 | **Launcher** | Unified dashboard and application launcher |

### Key Features

- **eBot AI Assistant** -- 33+ AI-powered actions including document summarization,
  data analysis, email drafting, meeting scheduling, and code generation
- **HMAC-SHA256 JWT Authentication** -- Secure multi-tenant auth with RBAC
- **Real-Time Collaboration** -- WebSocket-based operational transforms for
  simultaneous multi-user editing in eDocs, eSheets, and eSlides
- **Offline Support** -- Service worker caching and IndexedDB with conflict resolution
- **Cross-Platform** -- Browser, Electron desktop, responsive mobile web
- **75+ Tests** -- Unit, integration, and end-to-end test coverage
- **Plugin Architecture** -- Extensible through plugins

### Architecture

```
+--------------------------------------------------------------+
|                     Electron Shell                            |
|               (Desktop: Win / macOS / Linux)                  |
+--------------------------------------------------------------+
|                    React 18 Frontend                          |
|  +--------+ +--------+ +--------+ +--------+ +--------+     |
|  | eDocs  | |eSheets | |eSlides | | eNotes | | eMail  |     |
|  +--------+ +--------+ +--------+ +--------+ +--------+     |
|  +--------+ +--------+ +--------+ +--------+ +--------+     |
|  |  eDB   | | eDrive | |eConnect| | eForms | | eSway  |     |
|  +--------+ +--------+ +--------+ +--------+ +--------+     |
|  +--------+ +----------------------------------------------+ |
|  |ePlannr | |           eBot AI Engine                     | |
|  +--------+ |  33+ Actions | NLP | Context Awareness       | |
|             +----------------------------------------------+ |
+--------------------------------------------------------------+
|                  Express.js Backend                           |
|  REST API | WebSocket | Auth (JWT) | File Storage | DB       |
+--------------------------------------------------------------+
|              Data Layer                                       |
|   PostgreSQL | Redis | S3-compatible | Search Index           |
+--------------------------------------------------------------+
```

### Getting Started

```bash
git clone https://github.com/embeddedos-org/eOffice.git
cd eOffice
npm install
cp .env.example .env
npm run dev          # Frontend (Vite, port 5173)
npm run server       # Backend (Express, port 3001)
npm run electron:dev # Desktop app
npm test             # All 75+ tests
```

### eBot AI Actions

| Category | Actions | Description |
|----------|---------|-------------|
| Document | `summarize`, `expand`, `translate`, `rewrite` | AI text operations in eDocs |
| Spreadsheet | `analyze_data`, `create_formula`, `generate_chart` | Data intelligence in eSheets |
| Email | `draft_reply`, `categorize`, `extract_action_items` | Smart email in eMail |
| Presentation | `generate_outline`, `suggest_layout`, `add_visuals` | Design help in eSlides |
| Planning | `schedule_meeting`, `create_tasks`, `estimate_effort` | Project intelligence |
| General | `search_across_apps`, `create_workflow`, `export_report` | Cross-app AI features |
| Code | `generate_code`, `explain_code`, `debug_assist` | Developer tools via eBot |

### Authentication Flow

```
Client                    Server                    Database
  |                         |                         |
  |  POST /auth/login       |                         |
  |  {email, password}      |                         |
  |------------------------>|                         |
  |                         |  Verify credentials     |
  |                         |------------------------>|
  |                         |<------------------------|
  |                         |  Generate JWT           |
  |                         |  (HMAC-SHA256)          |
  |  {token, refreshToken}  |                         |
  |<------------------------|                         |
  |                         |                         |
  |  GET /api/docs          |                         |
  |  Authorization: Bearer  |                         |
  |------------------------>|                         |
  |                         |  Verify JWT + RBAC      |
  |  {documents[]}          |                         |
  |<------------------------|                         |
```

---

## Chapter 8: eVera -- AI Virtual Assistant

### Overview

**Repository:** `embeddedos-org/eVera`
**Backend:** Python (FastAPI + LangGraph)
**Desktop:** Electron
**Mobile:** React Native
**Version:** v0.9.0
**License:** MIT
**Status:** Active Development

eVera is a voice-first AI assistant with 24+ specialized agents and 183+ tools.
It features a 3D holographic avatar, multi-modal interaction, and a sophisticated
4-layer memory system.

### Key Features

- **24+ Specialized Agents** -- Domain-specific agents for productivity, health,
  finance, home automation, entertainment, coding, research, and more
- **183+ Tools** -- Calendar, email, web search, smart home, file management, coding
- **Voice Control** -- 3 modes (always-on, push-to-talk, wake-word), 19 languages
- **3D Holographic Avatar** -- Three.js-powered with lip sync and emotions
- **4-Layer Memory System** -- FAISS-powered: working, episodic, semantic, procedural
- **Tier-Based LLM Routing** -- Ollama (local), OpenAI, Google Gemini
- **Multi-Platform** -- FastAPI backend, Electron desktop, React Native mobile
- **Privacy-First** -- Local processing with Ollama for sensitive data

### Architecture

```
+--------------------------------------------------------------+
|                    Client Applications                        |
|  +----------+    +--------------+    +---------------+       |
|  | Electron |    | React Native |    | Web (React)   |       |
|  | Desktop  |    | Mobile App   |    | Progressive   |       |
|  +----------+    +--------------+    +---------------+       |
+--------------------------------------------------------------+
|                   FastAPI Backend                              |
|  +--------------------------------------------------------+  |
|  |              LangGraph Orchestrator                     |  |
|  |  +--------------------------------------------------+  |  |
|  |  |           24+ Specialized Agents                  |  |  |
|  |  |  Productivity | Health | Finance | Home           |  |  |
|  |  |  Entertainment | Coding | Research | ...          |  |  |
|  |  +--------------------------------------------------+  |  |
|  |  +--------------------------------------------------+  |  |
|  |  |             183+ Tools Library                    |  |  |
|  |  +--------------------------------------------------+  |  |
|  +--------------------------------------------------------+  |
|  +------------+  +-------------+  +------------------+       |
|  |  4-Layer   |  | Tier-Based  |  | Voice Pipeline   |       |
|  |  Memory    |  | LLM Router  |  | STT / TTS / NLP  |       |
|  |  (FAISS)   |  | Ollama/     |  | 19 Languages     |       |
|  |  Working   |  | OpenAI/     |  | 3 Voice Modes    |       |
|  |  Episodic  |  | Gemini      |  |                  |       |
|  |  Semantic  |  |             |  |                  |       |
|  |  Procedural|  |             |  |                  |       |
|  +------------+  +-------------+  +------------------+       |
+--------------------------------------------------------------+
|                 3D Avatar Engine (Three.js)                    |
|   Model Loading | Lip Sync | Emotions | Gestures | Idle      |
+--------------------------------------------------------------+
```

### Getting Started

```bash
git clone https://github.com/embeddedos-org/eVera.git
cd eVera/backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --host 0.0.0.0 --port 8000

# Desktop (separate terminal)
cd ../desktop && npm install && npm run dev

# Mobile (separate terminal)
cd ../mobile && npm install && npx expo start
```

### Agent Registry

| Agent | Domain | Key Tools |
|-------|--------|-----------|
| `productivity_agent` | Task/Calendar/Email | 15 tools |
| `health_agent` | Fitness/Nutrition/Sleep | 12 tools |
| `finance_agent` | Banking/Budget/Investing | 10 tools |
| `home_agent` | Smart Home/IoT | 14 tools |
| `entertainment_agent` | Music/Video/Games | 8 tools |
| `coding_agent` | IDE/Debug/Deploy | 18 tools |
| `research_agent` | Web Search/Papers/Data | 11 tools |
| `travel_agent` | Flights/Hotels/Itinerary | 9 tools |
| `shopping_agent` | Price Compare/Orders | 7 tools |
| `education_agent` | Tutoring/Quiz/Flashcards | 10 tools |
| `creative_agent` | Writing/Art/Music Gen | 8 tools |
| `social_agent` | Messaging/Social Media | 6 tools |

### Memory System API

```python
from evera.memory import MemoryManager

memory = MemoryManager(
    working_capacity=10,
    episodic_ttl_days=90,
    semantic_index="faiss",
    procedural_learning=True
)

memory.store_working("User asked about weather in Tokyo")
memory.store_episodic("User prefers metric temperature units")
memory.store_semantic("Tokyo average April temperature: 15C")
memory.store_procedural("weather_query", {
    "default_unit": "celsius",
    "include_forecast": True
})

context = memory.recall("What is the weather like?", top_k=5)
```

---

## Chapter 9: eApps -- Mobile App Platform

### Overview

**Repository:** `embeddedos-org/eApps`
**Language:** TypeScript, React Native
**License:** MIT
**Status:** Active Development

eApps is the mobile application platform for the EmbeddedOS ecosystem. Built on
React Native, it provides companion apps for EmbeddedOS hardware products, mobile
interfaces for eOffice and eVera, and a framework for building custom embedded
device companion applications.

### Key Features

- **Cross-Platform** -- Single codebase for iOS and Android
- **BLE Device Manager** -- Bluetooth Low Energy for EmbeddedOS hardware
- **Real-Time Data Sync** -- WebSocket and MQTT synchronization with eos devices
- **Offline-First** -- Local SQLite storage with background sync
- **Push Notifications** -- FCM/APNs for device alerts
- **Biometric Auth** -- Face ID, Touch ID, fingerprint
- **Theming Engine** -- Dynamic themes with WCAG 2.1 AA accessibility

### Architecture

```
+------------------------------------------------------+
|                 eApps Mobile Platform                 |
|  +----------+ +----------+ +------------------+      |
|  | eHealth  | | eOffice  | | eVera Mobile     |      |
|  | Companion| | Mobile   | | Assistant        |      |
|  +----------+ +----------+ +------------------+      |
+------------------------------------------------------+
|              React Native Core                        |
|  Navigation | State (Redux) | Forms | Charts          |
+----------+-----------+-----------+-------------------+
| BLE      | Network   | Storage   | Notifications     |
| Manager  | (REST/WS) | (SQLite)  | (FCM/APNs)        |
+----------+-----------+-----------+-------------------+
|            Native Modules (iOS / Android)             |
|  HealthKit | Camera | Sensors | Background Tasks      |
+------------------------------------------------------+
```

### Getting Started

```bash
git clone https://github.com/embeddedos-org/eApps.git
cd eApps && npm install
npx react-native run-ios     # iOS
npx react-native run-android  # Android
```

### API Highlights

| Module | API | Description |
|--------|-----|-------------|
| `@eapps/ble` | `BLEManager.scan()` | Scan for EmbeddedOS devices |
| `@eapps/ble` | `BLEManager.connect()` | Connect to device via BLE |
| `@eapps/sync` | `SyncEngine.start()` | Start real-time data sync |
| `@eapps/health` | `HealthData.getMetrics()` | Retrieve health metrics |
| `@eapps/auth` | `BiometricAuth.verify()` | Biometric authentication |

---

## Chapter 10: EoStudio -- Development Environment

### Overview

**Repository:** `embeddedos-org/EoStudio`
**Language:** TypeScript, Electron
**License:** MIT
**Status:** Active Development

EoStudio is the integrated development environment (IDE) for the EmbeddedOS ecosystem,
providing firmware development, hardware design review, and device debugging.

### Key Features

- **Multi-Language Editor** -- C, C++, Python, TypeScript, Pine Script support
- **Integrated Terminal** -- ebuild, OpenOCD, GDB integration
- **Hardware Debug** -- Register views, memory inspector, peripheral viewers
- **KiCad Viewer** -- Embedded schematic and PCB viewer
- **Device Manager** -- Detect, flash, monitor EmbeddedOS devices
- **EoSim Integration** -- Launch simulations from IDE
- **eBot Code Assistant** -- AI-powered code completion
- **Project Templates** -- Pre-configured for each EmbeddedOS repo

### Architecture

```
+----------------------------------------------------------+
|                   EoStudio IDE (Electron)                 |
|  +--------+ +------------+ +----------+ +------------+   |
|  | Editor | | Debug View | | Terminal | | KiCad View |   |
|  +--------+ +------------+ +----------+ +------------+   |
+----------------------------------------------------------+
|                Extension / Plugin System                  |
|  Language Servers | Debugger Adapters | Device Plugins    |
+----------------------------------------------------------+
|                    Core Services                          |
|  Project Manager | Build System | Device Manager | AI    |
+----------------------------------------------------------+
```

### Getting Started

```bash
git clone https://github.com/embeddedos-org/EoStudio.git
cd EoStudio && npm install && npm run build && npm run start
```

---

# Part III: Intelligence Layer

---

## Chapter 11: eAI -- AI/ML Inference Engine

### Overview

**Repository:** `embeddedos-org/eAI`
**Language:** C/C++, Python (training tools)
**License:** MIT
**Status:** Active Development

eAI is an AI/ML inference engine optimized for embedded devices, enabling on-device
ML inference without cloud connectivity.

### Key Features

- **Tiny Inference Runtime** -- Core under 64 KB ROM
- **Model Formats** -- TFLite Micro, ONNX Micro, custom eAI binary (INT8, FP16)
- **HW Acceleration** -- CMSIS-NN (Cortex-M), NEON (Cortex-A), RISC-V vector
- **Model Zoo** -- Keyword spotting, anomaly detection, image classification, health scoring
- **On-Device Training** -- Federated and transfer learning
- **Profiler** -- Per-layer timing, memory, accuracy metrics
- **Training Pipeline** -- PyTorch/TensorFlow with auto-quantization

### Architecture

```
+----------------------------------------------------------+
|              Python Training Pipeline                     |
|  PyTorch/TensorFlow | Quantization | Model Export         |
+----------------------------------------------------------+
|              eAI Model Compiler                           |
|  Graph Optimization | Operator Fusion | Memory Planning   |
+----------------------------------------------------------+
|              eAI Inference Runtime (C)                     |
|  +-----------+ +-----------+ +--------------------+       |
|  | Model     | | Operator  | | Memory Manager     |       |
|  | Loader    | | Registry  | | (Static/Dynamic)   |       |
|  +-----------+ +-----------+ +--------------------+       |
+----------------------------------------------------------+
|                  eos Integration                          |
|  Task | Timer | DMA | Accelerator Drivers                 |
+----------------------------------------------------------+
```

### Getting Started

```c
#include <eai/eai.h>
#include <eai/model.h>

int main(void) {
    eai_runtime_init();
    eai_model_t *model = eai_model_load("/flash/models/hr_quality.eai");

    float ppg_data[128];
    read_ppg_sensor(ppg_data, 128);
    eai_tensor_t input = { .data = ppg_data, .shape = {1, 128}, .dtype = EAI_FLOAT32 };
    eai_tensor_t output;
    eai_infer(model, &input, &output);

    printf("HR quality: %.2f\n", ((float *)output.data)[0]);
    eai_model_free(model);
    return 0;
}
```

### API Highlights

| Function | Description |
|----------|-------------|
| `eai_runtime_init()` | Initialize inference runtime |
| `eai_model_load()` | Load model from flash/file |
| `eai_infer()` | Run inference on input tensor |
| `eai_infer_async()` | Asynchronous inference with callback |
| `eai_profile()` | Profile inference performance |
| `eai_quantize()` | Dynamic quantization FP32 to INT8 |

### Ecosystem Use Cases

| Product | Use Case | Model Type |
|---------|----------|------------|
| eHealth365 Ring | HR/HRV/SpO2 scoring | Time-series classifier |
| eHealth365 Patch | Glucose prediction | LSTM regression |
| eRadar360 | Object detection | CNN + NMS |
| ePAM Vehicles | Path planning | Reinforcement learning |
| eVera | Wake word, NLU | Keyword spotter + NLP |
| eStocks | Pattern recognition | Transformer (quantized) |

---

## Chapter 12: eNI -- Neural Interface

### Overview

**Repository:** `embeddedos-org/eNI`
**Language:** C/C++, Python
**License:** MIT
**Status:** Research / Early Development

eNI is a biosignal processing library for neural and physiological signal acquisition,
filtering, feature extraction, and classification targeting EEG, EMG, ECG modalities.

### Key Features

- **Multi-Modal Acquisition** -- EEG (256 ch), EMG (16 ch), ECG (12 leads), EOG
- **Real-Time DSP** -- IIR/FIR filtering, FFT, wavelet transforms at 1 kHz
- **Feature Extraction** -- Time, frequency, time-frequency, connectivity features
- **BCI Paradigms** -- P300, SSVEP, motor imagery, hybrid BCI
- **eAI Integration** -- Raw signals to neural network classification pipeline
- **Artifact Rejection** -- Eye-blink, muscle, motion artifact removal
- **Data Export** -- EDF+, BDF, CSV, HDF5

### Architecture

```
+----------------------------------------------------------+
|                Application Layer                          |
|  BCI Control | Neurofeedback | Prosthetic Control | HMI  |
+----------------------------------------------------------+
|              Classification (eAI Integration)             |
|  SVM | LDA | CNN | LSTM | Ensemble | Transfer Learning   |
+----------------------------------------------------------+
|              Feature Extraction                           |
|  Time | Frequency | Time-Frequency | Connectivity         |
+----------------------------------------------------------+
|              Signal Processing                            |
|  Filtering | FFT | Wavelet | ICA | CSP | Artifact Reject |
+----------------------------------------------------------+
|              Signal Acquisition                           |
|  ADC Driver | ADS1299 | ADS1298 | OpenBCI | Custom       |
+----------------------------------------------------------+
```

### Getting Started

```c
#include <eni/eni.h>
#include <eni/filter.h>
#include <eni/feature.h>

void bci_pipeline(void) {
    eni_config_t cfg = { .channels=8, .sample_rate=250,
                         .adc_chip=ENI_ADC_ADS1299, .reference=ENI_REF_AVERAGE };
    eni_acq_t *acq = eni_acq_init(&cfg);
    eni_filter_t *bp = eni_filter_bandpass(8.0, 30.0, cfg.sample_rate, 4);

    float samples[8], filtered[8], features[16];
    while (1) {
        eni_acq_read(acq, samples);
        eni_filter_apply(bp, samples, filtered, 8);
        eni_feature_band_power(filtered, 8, cfg.sample_rate, features);
        execute_bci_command(classify_motor_imagery(features, 16));
    }
}
```

### API Highlights

| Function | Description |
|----------|-------------|
| `eni_acq_init()` | Initialize signal acquisition |
| `eni_acq_read()` | Read samples from ADC |
| `eni_filter_bandpass()` | Create bandpass IIR filter |
| `eni_filter_notch()` | Create notch filter (50/60 Hz) |
| `eni_fft()` | Compute FFT of signal segment |
| `eni_feature_band_power()` | Extract frequency band powers |
| `eni_artifact_detect()` | Detect and mark artifacts |
| `eni_export_edf()` | Export data in EDF+ format |

---

## Chapter 13: eStocks -- Algorithmic Trading

### Overview

**Repository:** `embeddedos-org/eStocks_Trading_Scripts`
**Language:** Python, Pine Script, thinkScript, EasyLanguage
**License:** MIT
**Status:** Active Development

eStocks is a comprehensive algorithmic trading system with 15 strategies, 7-layer
risk management, 7 data sources, 4 trading platforms, and 288+ tests.

### The 15 Strategies

| # | Strategy | Type | Description |
|---|----------|------|-------------|
| 1 | trend_following | Technical | Multi-timeframe EMA crossovers |
| 2 | breakout | Technical | Price breakout + volume confirm |
| 3 | mean_reversion | Statistical | Bollinger Band / z-score |
| 4 | factor | Quantitative | Value, momentum, quality, size |
| 5 | darvas_box | Technical | Darvas box breakout method |
| 6 | triple_screen | Technical | Elder triple screen system |
| 7 | canslim | Fundamental | CANSLIM growth stock selection |
| 8 | value | Fundamental | Deep value with margin of safety |
| 9 | ml | Machine Learning | Gradient boosting / random forest |
| 10 | rl | Reinforcement Learning | PPO/DQN trading agent |
| 11 | self_learning | Adaptive | Online learning + concept drift |
| 12 | sentiment | Alt Data | News/social sentiment analysis |
| 13 | earnings | Event-Driven | Earnings surprise + drift |
| 14 | sector_rotation | Macro | Economic cycle rotation |
| 15 | meta_ensemble | Ensemble | Meta-learner combining signals |

### 7-Layer Risk Management

```
+----------------------------------------------------------+
| Layer 7: Meta-Risk Orchestrator                          |
|   Circuit breakers, kill switch, cross-layer coordination |
+----------------------------------------------------------+
| Layer 6: Tail Risk Protection                            |
|   VaR/CVaR limits, black swan hedges                     |
+----------------------------------------------------------+
| Layer 5: Volatility Regime Detection                     |
|   GARCH modeling, regime switching, vol scaling           |
+----------------------------------------------------------+
| Layer 4: Drawdown Control                                |
|   Max drawdown limits, equity curve trading               |
+----------------------------------------------------------+
| Layer 3: Correlation Management                          |
|   Portfolio correlation matrix, diversification           |
+----------------------------------------------------------+
| Layer 2: Portfolio Heat                                  |
|   Risk budget, sector/asset exposure limits               |
+----------------------------------------------------------+
| Layer 1: Position Sizing                                 |
|   Kelly criterion, fixed fractional, ATR-based            |
+----------------------------------------------------------+
```

### Getting Started

```python
from estocks import TradingEngine, Strategy, RiskManager
from estocks.data import DataManager

data = DataManager(sources=['yahoo', 'alpha_vantage'])
data.load_universe(['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META'])

strategies = [
    Strategy('trend_following', weight=0.3),
    Strategy('mean_reversion', weight=0.2),
    Strategy('ml', weight=0.25),
    Strategy('meta_ensemble', weight=0.25)
]

risk = RiskManager(
    position_sizing='kelly',
    max_portfolio_heat=0.06,
    max_drawdown=0.15,
    var_confidence=0.99,
    circuit_breaker_loss=-0.05
)

engine = TradingEngine(strategies=strategies, risk_manager=risk, data_manager=data)
results = engine.backtest(start='2020-01-01', end='2026-04-01', initial_capital=100000)
print(f"Sharpe: {results.sharpe_ratio:.2f}, Return: {results.total_return:.2%}")
```

### Platform Deployment

| Platform | Language | Features |
|----------|----------|----------|
| TradingView | Pine Script v5 | Charts, alerts, strategy tester |
| thinkorswim | thinkScript | Scanning, options, custom studies |
| Interactive Brokers | Python (ibapi) | Full API, multi-asset, algo execution |
| TradeStation | EasyLanguage | RadarScreen, walk-forward optimization |

### Test Coverage: 288+ Tests

| Category | Tests |
|----------|-------|
| Strategy Unit Tests | 120 |
| Risk Management | 56 |
| Data Pipeline | 32 |
| Integration | 45 |
| Platform | 20 |
| Performance | 15 |

---

# Part IV: Hardware Products

---

## Chapter 14: eRadar360 -- Automotive Radar

### Overview

**Repository:** `embeddedos-org/eHardware-Designs-Products`
**Path:** `eHardware-Designs-Products/eRadar360/`
**Technology:** 77 GHz FMCW Radar, 10-layer hybrid PCB
**License:** MIT
**Status:** Development

eRadar360 is an automotive-grade ADAS radar module designed for 360-degree
environmental sensing using 77 GHz FMCW radar on a compact 120mm x 85mm
10-layer hybrid PCB.

### Key Specifications

| Parameter | Value |
|-----------|-------|
| Frequency Band | 76-81 GHz (77 GHz FMCW) |
| Board Dimensions | 120mm x 85mm |
| PCB Stack-up | 10-layer hybrid (RF + digital) |
| Range | 0.5m - 250m (long range), 0.2m - 30m (short range) |
| Field of View | +/-60 deg azimuth, +/-15 deg elevation |
| Range Resolution | 0.1m |
| Velocity Resolution | 0.1 m/s |
| Angular Resolution | 1 deg (azimuth), 5 deg (elevation) |
| TX Antennas | 3 (MIMO) |
| RX Antennas | 4 (MIMO) |
| Processing | ARM Cortex-R5 + DSP, running eos |
| Interface | CAN FD, Ethernet (100BASE-T1), SPI |
| Power | 4W typical, 6W peak |
| Temperature | -40C to +105C (AEC-Q100 Grade 1) |

### Architecture

```
+----------------------------------------------------------+
|                    eRadar360 Module                       |
|                                                          |
|  +----------------+    +----------------------------+    |
|  |  RF Frontend   |    |    Digital Backend          |    |
|  |                |    |                             |    |
|  |  TX Antennas   |    |  +----------------------+  |    |
|  |  (3x MIMO)     |    |  |  Radar SoC           |  |    |
|  |                |    |  |  ARM Cortex-R5 + DSP  |  |    |
|  |  RX Antennas   |    |  |  Running eos kernel   |  |    |
|  |  (4x MIMO)     |    |  |  + eAI inference      |  |    |
|  |                |    |  +----------------------+  |    |
|  |  77 GHz MMIC   |    |                             |    |
|  |  PA / LNA      |    |  CAN FD | Ethernet | SPI   |    |
|  +----------------+    +----------------------------+    |
|                                                          |
|  eBoot (secure boot) | Power Mgmt | EMC Filtering       |
+----------------------------------------------------------+
```

### Software Stack

The eRadar360 runs a complete EmbeddedOS software stack:

1. **eBoot** -- Secure boot with automotive-grade key management
2. **eos** -- RTOS kernel with deterministic scheduling for radar processing
3. **eAI** -- Object detection and classification neural network
4. **eIPC** -- Communication between radar processing and vehicle bus
5. **eDB** -- Configuration storage and calibration data

### Getting Started

```bash
cd eHardware-Designs-Products/eRadar360
kicad eRadar360.kicad_pro        # Open hardware design
ebuild analyze --bom eRadar360   # Generate BOM
ebuild analyze --drc eRadar360   # Run design rule checks
ebuild build eRadar360_firmware --target cortex-r5  # Build firmware
ebuild flash eRadar360_firmware --probe jlink       # Flash via JTAG
```

---

## Chapter 15: eHealth365 -- Health Monitoring

### Overview

**Repository:** `embeddedos-org/eHardware-Designs-Products`
**Path:** `eHardware-Designs-Products/eHealth365/`
**Products:** Smart Ring Pro, Smart Patch Pro, Mobile App
**License:** MIT
**Status:** Development

eHealth365 is a comprehensive health monitoring ecosystem achieving approximately
90% coverage of clinically relevant health metrics through two wearable devices and
a companion mobile application.

### Smart Ring Pro

| Parameter | Value |
|-----------|-------|
| Form Factor | Titanium ring, 8mm width, sizes 6-13 |
| Sensors | PPG (HR/HRV/SpO2), skin temperature, 6-axis IMU |
| Processor | nRF52840 (ARM Cortex-M4F), running eos |
| Connectivity | BLE 5.3 |
| Battery | 20 mAh Li-Po, 5-7 day battery life |
| Charging | Wireless (Qi-compatible cradle) |
| Water Resistance | IP68, 50m swim-proof |
| Weight | 4-6g (depending on size) |

**Health Metrics:** Heart Rate (continuous 24/7), HRV (stress/recovery/ANS),
SpO2, Skin Temperature, Sleep Stages (wake/light/deep/REM), Activity Tracking,
Respiratory Rate, Readiness Score.

### Smart Patch Pro

| Parameter | Value |
|-----------|-------|
| Form Factor | 45mm x 30mm x 3mm adhesive patch |
| Sensors | CGM glucose (14-day), sweat electrolytes, monthly blood cartridge |
| Processor | STM32H743 (ARM Cortex-M7), running eos |
| Connectivity | BLE 5.3, NFC |
| Battery | 120 mAh Li-Po, 14-day life |
| Adhesive | Medical-grade, hypoallergenic, 14-day wear |

**Health Metrics:** Continuous Glucose (CGM), Sweat Electrolytes
(Na/K/Cl/lactate), Monthly Blood Panel (lipids, HbA1c, CRP, vitamin D, CBC),
Hydration Level, Metabolic Rate.

### Combined Health Coverage (~90%)

```
+--------------------------------------------------------------+
|                    eHealth365 Ecosystem                       |
|                                                              |
|  Smart Ring Pro              Smart Patch Pro                 |
|  +------------------+       +----------------------------+  |
|  | Heart Rate       |       | Glucose (CGM, 14-day)      |  |
|  | HRV              |       | Sweat Electrolytes         |  |
|  | SpO2             |       | Monthly Blood Panel        |  |
|  | Temperature      |       | Hydration                  |  |
|  | Sleep Stages     |       | Metabolic Rate             |  |
|  | Activity         |       |                            |  |
|  | Respiratory Rate |       |                            |  |
|  | Readiness Score  |       |                            |  |
|  +------------------+       +----------------------------+  |
|                                                              |
|               eApps Mobile Companion                         |
|  +----------------------------------------------------------+|
|  | Dashboard | Trends | Alerts | Reports | Sharing          ||
|  | eAI Health Scoring | Risk Prediction | Coaching          ||
|  +----------------------------------------------------------+|
+--------------------------------------------------------------+
```

### Pricing

| Item | Price |
|------|-------|
| Smart Ring Pro | $399 |
| Smart Patch Pro (starter kit) | $299 |
| CGM Sensor Refill (14-day, 2-pack) | $79 |
| Blood Cartridge (monthly, 1-pack) | $49 |
| **First Year Total** | **~$1,100** |

### Software Stack

Each eHealth365 device runs the full EmbeddedOS platform stack:

- **eBoot** -- Secure boot with firmware update over BLE
- **eos** -- RTOS with low-power optimizations for multi-day battery life
- **eAI** -- On-device health metric scoring and anomaly detection
- **eIPC** -- Inter-sensor data fusion between ring and patch
- **eDB** -- Local health data storage with encryption at rest
- **eApps** -- React Native companion app (Chapter 9)

### Getting Started

```bash
ebuild build smart_ring --target nrf52840    # Build ring firmware
ebuild build smart_patch --target stm32h743  # Build patch firmware
cd ../../eApps && npm install                # Build companion app
npx react-native run-ios
```

---

## Chapter 16: ePAM -- Personal Air Mobility

### Overview

**Repository:** `embeddedos-org/eHardware-Designs-Products`
**Path:** `eHardware-Designs-Products/ePAM/`
**Products:** Eco Car, Urban Drone eVTOL, Space Shuttle, Combo Unit
**License:** MIT
**Status:** Concept / Early Development

ePAM (Personal Air Mobility) is EmbeddedOS's most ambitious hardware project:
a family of 4 vehicles spanning ground, air, and space transportation powered
by hybrid renewable energy and running EmbeddedOS for autonomous operation.

### Vehicle Lineup

#### 1. Eco Car ($28,000 - $45,000)

| Parameter | Value |
|-----------|-------|
| Type | Ground electric vehicle |
| Range | 400-600 km (battery + solar) |
| Top Speed | 180 km/h |
| Power | Solar + battery + H2 fuel cell |
| Autonomy | Level 3 (highway), Level 2 (urban) |
| Passengers | 4-5 |
| Energy Recovery | Regen braking + kinetic recovery |

#### 2. Urban Drone eVTOL ($85,000 - $120,000)

| Parameter | Value |
|-----------|-------|
| Type | Electric vertical takeoff and landing |
| Range | 80-150 km |
| Top Speed | 250 km/h |
| Cruise Altitude | 300-600m AGL |
| Power | Battery + solar + H2 backup |
| Autonomy | Level 4 (fully autonomous urban) |
| Passengers | 1-2 |
| Rotors | 8 (octocopter, redundant) |

#### 3. Space Shuttle -- Suborbital ($2M - $4M)

| Parameter | Value |
|-----------|-------|
| Type | Suborbital spacecraft |
| Altitude | Up to 100 km (Karman line) |
| Flight Duration | 15-30 minutes |
| Power | H2/O2 propulsion + solar + battery |
| Passengers | 2-4 |
| Reusability | Fully reusable, vertical landing |
| G-Forces | Max 3.5g ascent, 1.5g descent |

#### 4. Combo Unit -- Trans-Atmospheric ($5M - $9M)

| Parameter | Value |
|-----------|-------|
| Type | Multi-mode: ground + air + suborbital |
| Ground Range | 600 km |
| Air Range | 200 km (eVTOL mode) |
| Suborbital | Point-to-point up to 10,000 km |
| Power | Full hybrid: solar + H2 + battery + kinetic regen |
| Autonomy | Level 5 (all domains) |
| Passengers | 2-4 |
| Transformation | Automated mode switching (ground/air/space) |

### Power System Architecture

```
+--------------------------------------------------------------+
|                  ePAM Hybrid Power System                     |
|                                                              |
|  +------------+  +------------+  +--------------------+      |
|  |   Solar    |  |  H2 Fuel   |  |  Li-Ion Battery    |      |
|  |   Panels   |  |  Cell      |  |  Pack (modular)    |      |
|  |  (body-    |  |  (PEM)     |  |                    |      |
|  |  integrated|  |            |  |                    |      |
|  +------+-----+  +------+----+  +--------+-----------+      |
|         |               |                 |                  |
|         +---------------+-----------------+                  |
|                         |                                    |
|              +----------+----------+                         |
|              | Power Management    |                         |
|              | Unit (eos-based)    |                         |
|              +----------+----------+                         |
|                         |                                    |
|         +---------------+-----------------+                  |
|         |               |                 |                  |
|  +------+-----+  +-----+------+  +-------+----------+      |
|  |  Motors /  |  | Avionics   |  |  Kinetic Energy  |      |
|  |  Propulsion|  | & Compute  |  |  Recovery        |      |
|  +------------+  +------------+  +------------------+      |
+--------------------------------------------------------------+
```

### Software Stack

All ePAM vehicles run EmbeddedOS with safety-critical extensions:

- **eBoot** -- Secure boot with redundant paths (triple for Space Shuttle)
- **eos** -- RTOS with ASIL-D safety extensions for automotive/aerospace
- **eAI** -- Autonomous navigation, obstacle detection, path planning
- **eRadar360** -- Environmental sensing (integrated in all vehicles)
- **eIPC** -- Vehicle bus (CAN FD, ARINC 429 for aerospace)
- **eDB** -- Flight data recording, telemetry storage
- **eApps** -- Passenger mobile app for vehicle control

### Getting Started

```bash
cd eHardware-Designs-Products/ePAM
kicad eco_car/eco_car.kicad_pro              # Open design
eosim launch --vehicle eco_car --scenario highway  # Simulate
ebuild build epam_flight_ctrl --target cortex-r5 --safety asil-d
```

---

# Part V: Development and Operations

---

## Chapter 17: EoSim -- Simulation Environment

### Overview

**Repository:** `embeddedos-org/EoSim`
**Language:** C++, Python
**License:** MIT
**Status:** Active Development

EoSim is a comprehensive hardware-software co-simulation environment for the
EmbeddedOS ecosystem. It enables developers to test firmware, validate hardware
designs, and simulate complete systems before physical prototyping.

### Key Features

- **Instruction-Set Simulation** -- Cycle-accurate ARM Cortex-M/R/A and RISC-V ISS
  with peripheral modeling
- **Hardware-in-the-Loop (HIL)** -- Connect simulated firmware to real hardware
  peripherals via USB/JTAG bridges
- **Sensor Simulation** -- Synthetic data for accelerometers, gyroscopes, PPG,
  glucose, radar returns
- **Vehicle Dynamics** -- Physics-based simulation for ePAM ground, air, space vehicles
- **Network Simulation** -- BLE, Wi-Fi, CAN, Ethernet with configurable parameters
- **Power Modeling** -- Estimate power consumption and battery life from execution traces
- **Fault Injection** -- Simulate bit flips, stuck pins, sensor drift for reliability
- **Visualization** -- Real-time 3D visualization of simulated devices and environments

### Architecture

```
+--------------------------------------------------------------+
|                    EoSim Framework                            |
|  +----------------------------------------------------------+|
|  |              Simulation Manager                           ||
|  |  Scenario Config | Clock Sync | Event Scheduler           ||
|  +----------------------------------------------------------+|
|  +--------+ +--------+ +------------+ +---------------+      |
|  | CPU    | | Periph | | Sensor     | | Network       |      |
|  | Sim    | | Models | | Models     | | Sim           |      |
|  | (ISS)  | | (GPIO, | | (PPG,IMU, | | (BLE,CAN,    |      |
|  | ARM/RV | |  SPI)  | |  Radar)   | |  Ethernet)    |      |
|  +--------+ +--------+ +------------+ +---------------+      |
|  +------------+ +---------------+ +------------------+       |
|  | Vehicle    | | Power         | | Fault            |       |
|  | Dynamics   | | Modeling      | | Injection        |       |
|  +------------+ +---------------+ +------------------+       |
|  +----------------------------------------------------------+|
|  |           3D Visualization (OpenGL / WebGL)               ||
|  +----------------------------------------------------------+|
+--------------------------------------------------------------+
```

### Getting Started

```bash
git clone https://github.com/embeddedos-org/EoSim.git
cd EoSim && mkdir build && cd build
cmake .. -DEOSIM_ENABLE_3D=ON
make -j$(nproc)
eosim launch --config scenarios/eHealth365_ring.yaml
```

### Example Scenario Configuration

```yaml
scenario:
  name: "Smart Ring 24hr Simulation"
  duration: 86400
  time_scale: 100

target:
  cpu: nrf52840
  firmware: ../eos/build/eHealth365_ring.elf
  bootloader: ../eBoot/build/eHealth365_ring_boot.bin

sensors:
  ppg:
    model: synthetic_ppg
    heart_rate_bpm: [55, 60, 72, 85, 120, 72, 58]
    noise_level: 0.05
  imu:
    model: human_wrist
    activity_pattern: [sleep, sedentary, walking, running, sedentary, sleep]
  temperature:
    model: circadian
    baseline_c: 36.5

power:
  battery_mah: 20
  measure_interval_ms: 100

faults:
  - type: sensor_drift
    sensor: ppg
    start_time: 43200
    magnitude: 0.1
```

### API Highlights

| Function | Description |
|----------|-------------|
| `eosim_create()` | Create simulation instance |
| `eosim_load_firmware()` | Load firmware ELF into CPU simulator |
| `eosim_add_sensor()` | Add simulated sensor model |
| `eosim_inject_fault()` | Schedule fault injection event |
| `eosim_run()` | Run simulation for specified duration |
| `eosim_get_power_trace()` | Extract power consumption trace |
| `eosim_export_waveform()` | Export signal waveforms (VCD format) |

---

## Chapter 18: Cross-Product Integration

### Overview

The true power of EmbeddedOS emerges when products work together. This chapter
documents the integration points, dependency relationships, and data flows
between all 16 repositories.

### Dependency Graph

```
                    +---------------------+
                    |  embeddedos-org      |
                    |  .github.io (docs)   |
                    +----------+----------+
                               |  documents
                               v
+--------------------------------------------------------------+
|                                                              |
|  +------+    +------+    +------+                            |
|  | eos  |<---| eBoot|    |ebuild|--- builds all ---+         |
|  |kernel|    | boot |    |build |                  |         |
|  +--+---+    +--+---+    +--+---+                  |         |
|     |           |           |                      |         |
|     |    +------+     +-----+                      |         |
|     v    v            v                            |         |
|  +----------+   +----------+   +----------+        |         |
|  |  eIPC   |   |  eDB    |   |  eAI    |        |         |
|  |  comms  |   |  storage |   |  infer  |        |         |
|  +----+----+   +----+-----+   +----+----+        |         |
|       |              |              |              |         |
|       +--------------+--------------+              |         |
|                      |                             |         |
|         +------------+-------------+               |         |
|         v            v             v               |         |
|  +----------+  +----------+  +--------------+      |         |
|  | eBrowser |  | eOffice  |  | eVera        |      |         |
|  +----------+  +----------+  +--------------+      |         |
|                                                    |         |
|  +----------+  +----------+  +--------------+      |         |
|  | eNI      |  | eApps   |  | eStocks      |      |         |
|  +----------+  +----------+  +--------------+      |         |
|                                                    |         |
|  +----------------------------------------------+  |         |
|  |          eHardware-Designs-Products           |  |         |
|  |  eRadar360 | eHealth365 | ePAM Vehicles      |<-+         |
|  +----------------------------------------------+            |
|                                                              |
|  +----------+  +----------+                                  |
|  | EoStudio |  | EoSim   |                                  |
|  +----------+  +----------+                                  |
+--------------------------------------------------------------+
```

### Key Integration Patterns

#### 1. Hardware Product Stack

Every EmbeddedOS hardware product uses this foundational stack:

```
Application Code (product-specific)
        |
        v
+---------------+
|    eAI        |  <-- On-device ML inference
+---------------+
|    eDB        |  <-- Local data storage
+---------------+
|    eIPC       |  <-- Inter-process communication
+---------------+
|    eos        |  <-- RTOS kernel & drivers
+---------------+
|    eBoot      |  <-- Secure bootloader
+---------------+
        |
    Hardware (PCB designed in eHardware-Designs-Products)
```

#### 2. AI Pipeline Integration

```
Raw Sensor Data (eHealth365 / eRadar360 / eNI)
        |
        v
Signal Processing (eNI for biosignals, eos DSP for radar)
        |
        v
Feature Extraction (eNI / custom)
        |
        v
eAI Inference (on-device model)
        |
        v
Result Publication (via eIPC)
        |
        +---> eDB (store results)
        +---> eApps (display to user)
        +---> eVera (voice alerts)
```

#### 3. Development Workflow Integration

```
Developer writes code
        |
        v
EoStudio (IDE with IntelliSense + debug)
        |
        v
ebuild (compile + link + package)
        |
        v
EoSim (simulate on virtual hardware)
        |
        v
ebuild flash (deploy to real hardware)
        |
        v
EoStudio debug (JTAG/SWD live debug)
```

#### 4. eVera Cross-Product Voice Control

```
User Voice Command
        |
        v
eVera Voice Pipeline (STT -> NLU -> Intent)
        |
        +---> "Check my heart rate" -> eApps -> eHealth365
        +---> "Create a document"  -> eOffice eDocs
        +---> "Show me the radar"  -> eApps -> eRadar360
        +---> "Check my portfolio" -> eStocks API
        +---> "Open browser"       -> eBrowser
        +---> "Run simulation"     -> EoSim
```

### Integration Matrix

| From / To | eos | eBoot | eAI | eIPC | eDB |
|-----------|-----|-------|-----|------|-----|
| **eHealth365** | kernel | boot | scoring | sensor bus | health data |
| **eRadar360** | kernel | boot | detection | vehicle bus | config |
| **ePAM** | kernel | boot | navigation | vehicle bus | telemetry |
| **eBrowser** | PAL | -- | -- | content | cache |
| **eOffice** | -- | -- | eBot | -- | documents |
| **eVera** | -- | -- | NLU | -- | memory |

---

# Part VI: Organization

---

## Chapter 19: Governance and Contribution Model

### Organization Structure

| Role | Responsibilities |
|------|-----------------|
| **Project Lead** | Overall vision, architecture decisions, release management |
| **Repo Maintainers** | Per-repo code review, issue triage, release tagging |
| **Core Contributors** | Regular contributors with commit access |
| **Contributors** | Anyone who submits PRs, bug reports, or documentation |
| **Community Members** | Users, testers, discussion participants |

### Contribution Workflow

```
1. Fork the repository
2. Create a feature branch: git checkout -b feature/my-feature
3. Make changes following coding standards
4. Write tests (minimum 80% coverage for new code)
5. Run linting: ebuild lint && ebuild format
6. Commit with conventional commits: git commit -m "feat(module): description"
7. Push and create a Pull Request
8. Address review comments
9. Maintainer merges after approval
```

### Coding Standards

| Language | Style Guide | Formatter | Linter |
|----------|------------|-----------|--------|
| C/C++ | EmbeddedOS C Style (LLVM) | clang-format | clang-tidy, cppcheck |
| Python | PEP 8 + Black | Black | flake8, mypy |
| TypeScript | ESLint + Prettier | Prettier | ESLint |
| Pine Script | EmbeddedOS Pine Style | -- | Custom linter |

### Versioning

All repositories follow Semantic Versioning (SemVer):

- **MAJOR** -- Breaking API changes
- **MINOR** -- New features, backward-compatible
- **PATCH** -- Bug fixes, backward-compatible

### Communication Channels

| Channel | Purpose |
|---------|---------|
| GitHub Discussions | Technical discussions, Q&A, RFCs |
| GitHub Issues | Bug reports, feature requests |
| Discord Server | Real-time chat, community support |
| Monthly Dev Call | Architecture review, roadmap planning |
| Blog (GitHub Pages) | Release announcements, tutorials |

### License

All repositories are released under the **MIT License**.

---

## Chapter 20: embeddedos-org.github.io -- The Documentation Hub

### Overview

**Repository:** `embeddedos-org/embeddedos-org.github.io`
**Technology:** GitHub Pages, Markdown, Jekyll/Hugo
**License:** MIT
**Status:** Active

The documentation hub is the central website and documentation portal for the
entire EmbeddedOS ecosystem, aggregating docs from all 16 repositories.

### Key Features

- **Unified Documentation** -- All product docs in one place
- **API Reference** -- Auto-generated from source code
- **Tutorials** -- Step-by-step guides for each product
- **Architecture Diagrams** -- Visual system documentation
- **Search** -- Full-text search across all docs
- **Version Selector** -- Docs versioned per release
- **Blog** -- Release notes, engineering posts
- **Community Showcase** -- Projects built with EmbeddedOS

### Site Structure

```
embeddedos-org.github.io/
|-- index.html                  # Landing page
|-- docs/
|   |-- eos/                    # eos documentation
|   |-- eboot/                  # eBoot documentation
|   |-- ebuild/                 # ebuild documentation
|   |-- eipc/                   # eIPC documentation
|   |-- edb/                    # eDB documentation
|   |-- ebrowser/               # eBrowser documentation
|   |-- eoffice/                # eOffice documentation
|   |-- evera/                  # eVera documentation
|   |-- eai/                    # eAI documentation
|   |-- eni/                    # eNI documentation
|   |-- estocks/                # eStocks documentation
|   |-- ehardware/              # eHardware documentation
|   |-- eapps/                  # eApps documentation
|   |-- eosim/                  # EoSim documentation
|   |-- eostudio/               # EoStudio documentation
|   +-- ecosystem-guide.md      # THIS DOCUMENT
|-- api/                        # Auto-generated API reference
|-- tutorials/                  # Step-by-step tutorials
|-- blog/                       # Engineering blog
+-- community/                  # Community projects
```

### Getting Started

```bash
git clone https://github.com/embeddedos-org/embeddedos-org.github.io.git
cd embeddedos-org.github.io
bundle install
bundle exec jekyll serve --livereload
# Visit http://localhost:4000
```

---

# Appendices

---

## Appendix A: Repository Quick Reference

| # | Repository | Language(s) | Description | Status |
|---|-----------|-------------|-------------|--------|
| 1 | eos | C/C++ | Embedded RTOS kernel, HAL, device drivers | Active |
| 2 | eBoot | C/Assembly | Secure bootloader with board ports | Active |
| 3 | ebuild | Python/CMake | Build system + KiCad HW analyzer | Active |
| 4 | eBrowser | C/C++ | Lightweight embedded web browser | Active |
| 5 | eOffice | TypeScript/JS | AI-powered office suite (12 apps) | Active |
| 6 | eVera | Python/TS/JS | Voice-first AI assistant (24+ agents) | Active |
| 7 | eStocks_Trading_Scripts | Python/Pine/thinkScript | Algorithmic trading (15 strategies) | Active |
| 8 | eHardware-Designs-Products | KiCad/C | Hardware (eRadar360, eHealth365, ePAM) | Development |
| 9 | eAI | C/C++/Python | AI/ML inference engine for embedded | Active |
| 10 | eNI | C/C++/Python | Neural interface, biosignal processing | Research |
| 11 | eIPC | C/C++ | Inter-process communication library | Active |
| 12 | eDB | C | Embedded database engine | Active |
| 13 | eApps | TypeScript/RN | Mobile app platform (React Native) | Active |
| 14 | EoSim | C++/Python | Hardware/software simulation | Active |
| 15 | EoStudio | TypeScript | Integrated development environment | Active |
| 16 | embeddedos-org.github.io | Markdown/HTML | Organization website and docs | Active |

---

## Appendix B: Technology Stack Summary

### Languages

| Language | Usage | Repositories |
|----------|-------|-------------|
| C | Kernel, drivers, bootloader, database, IPC | eos, eBoot, eDB, eIPC, eAI, eNI |
| C++ | Browser engine, simulation, inference | eBrowser, EoSim, eAI, eNI |
| Python | Build tools, trading, AI training, backend | ebuild, eStocks, eAI, eNI, eVera |
| TypeScript | Web apps, IDE, mobile apps | eOffice, EoStudio, eApps, eVera |
| JavaScript | Frontend, Electron apps | eOffice, eBrowser (JS engine), eVera |
| Assembly | Bootloader, context switch | eBoot, eos |
| Pine Script | TradingView strategies | eStocks |
| thinkScript | thinkorswim strategies | eStocks |
| EasyLanguage | TradeStation strategies | eStocks |

### Key Frameworks and Libraries

| Framework/Library | Version | Used By |
|-------------------|---------|---------|
| React | 18.x | eOffice, eVera (desktop) |
| React Native | 0.73+ | eApps, eVera (mobile) |
| Express.js | 4.x | eOffice |
| FastAPI | 0.100+ | eVera |
| LangGraph | latest | eVera |
| Electron | 28+ | eOffice, eVera, EoStudio |
| Vite | 5.x | eOffice |
| SDL2 | 2.28+ | eBrowser |
| LVGL | 9.2 | eBrowser |
| Three.js | latest | eVera (3D avatar) |
| FAISS | latest | eVera (memory) |
| TFLite Micro | 2.x | eAI |
| lwIP | 2.1+ | eos |
| mbedTLS | 3.x | eos, eBoot |
| CMake | 3.20+ | eos, eBoot, eBrowser, eAI, eNI, EoSim |
| Protocol Buffers | 3.x | eIPC |

### Testing Frameworks

| Framework | Language | Used By | Tests |
|-----------|----------|---------|-------|
| Unity (C) | C | eos, eBoot, eIPC, eDB | ~200+ |
| Google Test | C++ | eBrowser, eAI, EoSim | ~200+ |
| Jest | TS/JS | eOffice, eApps, EoStudio | ~100+ |
| pytest | Python | eStocks, eVera, eAI | ~350+ |
| React Testing Library | TS | eOffice, eApps | ~50+ |
| Detox | React Native | eApps | ~30+ |

---

## Appendix C: Getting Started Guide

### Prerequisites

- **Git** (2.30+)
- **Python** (3.10+)
- **Node.js** (18+) and npm (9+)
- **CMake** (3.20+)
- **C/C++ Compiler** -- GCC 12+ or Clang 15+
- **ARM Toolchain** -- arm-none-eabi-gcc 13+ (for embedded targets)

### Per-Repository Quickstart

```bash
# eos -- Embedded OS
git clone https://github.com/embeddedos-org/eos.git && cd eos
ebuild setup && ebuild build blinky --board stm32f4_disco --debug
ebuild flash blinky --probe stlink

# eBoot -- Bootloader
git clone https://github.com/embeddedos-org/eBoot.git && cd eBoot
ebuild build --board stm32f4_disco && ebuild flash --probe stlink --stage1

# ebuild -- Build System
git clone https://github.com/embeddedos-org/ebuild.git && cd ebuild
pip install -e . && ebuild --version

# eIPC -- Inter-Process Communication
git clone https://github.com/embeddedos-org/eIPC.git && cd eIPC
mkdir build && cd build && cmake .. -DEIPC_BUILD_TESTS=ON
make -j$(nproc) && ctest --output-on-failure

# eDB -- Embedded Database
git clone https://github.com/embeddedos-org/eDB.git && cd eDB
mkdir build && cd build && cmake .. -DEDB_BUILD_TESTS=ON
make -j$(nproc) && ctest --output-on-failure

# eBrowser -- Web Browser
git clone https://github.com/embeddedos-org/eBrowser.git && cd eBrowser
mkdir build && cd build
cmake .. -DEBROWSER_BACKEND=SDL2 -DCMAKE_BUILD_TYPE=Debug
make -j$(nproc) && ctest  # 130+ tests

# eOffice -- Office Suite
git clone https://github.com/embeddedos-org/eOffice.git && cd eOffice
npm install && cp .env.example .env
npm run dev && npm test  # 75+ tests

# eVera -- AI Assistant
git clone https://github.com/embeddedos-org/eVera.git
cd eVera/backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt && cp .env.example .env
uvicorn main:app --port 8000

# eAI -- AI/ML Inference
git clone https://github.com/embeddedos-org/eAI.git && cd eAI
mkdir build && cd build && cmake .. -DEAI_BUILD_TESTS=ON
make -j$(nproc) && ctest

# eNI -- Neural Interface
git clone https://github.com/embeddedos-org/eNI.git && cd eNI
mkdir build && cd build && cmake .. -DENI_BUILD_TESTS=ON
make -j$(nproc) && ctest

# eStocks -- Trading
git clone https://github.com/embeddedos-org/eStocks_Trading_Scripts.git
cd eStocks_Trading_Scripts && pip install -r requirements.txt
pytest tests/ -v  # 288+ tests

# eApps -- Mobile
git clone https://github.com/embeddedos-org/eApps.git && cd eApps
npm install && npx react-native run-ios

# EoSim -- Simulation
git clone https://github.com/embeddedos-org/EoSim.git && cd EoSim
mkdir build && cd build && cmake .. -DEOSIM_ENABLE_3D=ON
make -j$(nproc)

# EoStudio -- IDE
git clone https://github.com/embeddedos-org/EoStudio.git && cd EoStudio
npm install && npm run build && npm run start

# eHardware-Designs-Products
git clone https://github.com/embeddedos-org/eHardware-Designs-Products.git
cd eHardware-Designs-Products
kicad eRadar360/eRadar360.kicad_pro  # Requires KiCad 7+

# Documentation Hub
git clone https://github.com/embeddedos-org/embeddedos-org.github.io.git
cd embeddedos-org.github.io
bundle install && bundle exec jekyll serve --livereload
```

---

## Glossary

| Term | Definition |
|------|-----------|
| **ADAS** | Advanced Driver Assistance System -- automotive safety features |
| **ADC** | Analog-to-Digital Converter -- converts analog signals to digital values |
| **AEC-Q100** | Automotive Electronics Council qualification standard for ICs |
| **ASIL** | Automotive Safety Integrity Level -- ISO 26262 safety classification |
| **BCI** | Brain-Computer Interface -- direct communication between brain and device |
| **BLE** | Bluetooth Low Energy -- low-power wireless communication protocol |
| **BOM** | Bill of Materials -- list of components needed to build a product |
| **BSP** | Board Support Package -- hardware-specific drivers and configuration |
| **CAN FD** | Controller Area Network Flexible Data-rate -- automotive bus protocol |
| **CGM** | Continuous Glucose Monitoring -- real-time glucose measurement |
| **CMSIS-NN** | Cortex Microcontroller Software Interface Standard for Neural Networks |
| **CSP** | Common Spatial Pattern -- spatial filtering for EEG analysis |
| **CVaR** | Conditional Value at Risk -- expected loss beyond VaR threshold |
| **DAC** | Digital-to-Analog Converter |
| **DRC** | Design Rule Check -- automated PCB layout verification |
| **DVFS** | Dynamic Voltage and Frequency Scaling -- power optimization technique |
| **EDF+** | European Data Format -- standard for biosignal recordings |
| **eVTOL** | Electric Vertical Takeoff and Landing aircraft |
| **FAISS** | Facebook AI Similarity Search -- vector similarity search library |
| **FMCW** | Frequency-Modulated Continuous Wave -- radar modulation technique |
| **FOTA** | Firmware Over-The-Air -- wireless firmware update mechanism |
| **GARCH** | Generalized Autoregressive Conditional Heteroskedasticity |
| **GPIO** | General Purpose Input/Output -- configurable digital pin |
| **HAL** | Hardware Abstraction Layer -- uniform API across hardware platforms |
| **HIL** | Hardware-in-the-Loop -- simulation technique connecting real and virtual HW |
| **HMAC** | Hash-based Message Authentication Code |
| **HRV** | Heart Rate Variability -- variation in time between heartbeats |
| **HSM** | Hardware Security Module -- dedicated cryptographic processor |
| **I2C** | Inter-Integrated Circuit -- two-wire serial communication bus |
| **ICA** | Independent Component Analysis -- signal separation technique |
| **ISS** | Instruction Set Simulator -- software CPU emulator |
| **JWT** | JSON Web Token -- compact token format for authentication |
| **KiCad** | Open-source electronics design automation (EDA) software |
| **LangGraph** | Framework for building stateful multi-agent AI applications |
| **LSTM** | Long Short-Term Memory -- recurrent neural network architecture |
| **LVGL** | Light and Versatile Graphics Library -- embedded GUI framework |
| **lwIP** | Lightweight IP -- small TCP/IP stack for embedded systems |
| **MMIC** | Monolithic Microwave Integrated Circuit -- RF chip |
| **MQTT** | Message Queuing Telemetry Transport -- lightweight messaging protocol |
| **MPU** | Memory Protection Unit -- hardware memory access control |
| **NLU** | Natural Language Understanding -- AI text comprehension |
| **NMS** | Non-Maximum Suppression -- object detection post-processing |
| **OTP** | One-Time Programmable -- fuses that can only be written once |
| **PAL** | Platform Abstraction Layer |
| **PEM** | Proton Exchange Membrane -- hydrogen fuel cell technology |
| **PPG** | Photoplethysmography -- optical heart rate sensing technique |
| **QoS** | Quality of Service -- communication reliability level |
| **RBAC** | Role-Based Access Control -- permission model |
| **RPC** | Remote Procedure Call -- inter-process function invocation |
| **RTOS** | Real-Time Operating System -- OS with deterministic timing |
| **SBOM** | Software Bill of Materials -- list of software components |
| **SDL2** | Simple DirectMedia Layer -- cross-platform multimedia library |
| **SPI** | Serial Peripheral Interface -- synchronous serial bus |
| **SpO2** | Peripheral Blood Oxygen Saturation |
| **SSVEP** | Steady-State Visual Evoked Potential -- BCI paradigm |
| **STT** | Speech-to-Text -- voice recognition |
| **TLS** | Transport Layer Security -- cryptographic network protocol |
| **TPM** | Trusted Platform Module -- hardware security chip |
| **TTS** | Text-to-Speech -- voice synthesis |
| **UART** | Universal Asynchronous Receiver-Transmitter -- serial interface |
| **VaR** | Value at Risk -- maximum expected loss at confidence level |
| **WAL** | Write-Ahead Logging -- database crash recovery technique |

---

*End of The EmbeddedOS Ecosystem -- Complete Product Guide*

*First Edition, April 2026*

*Copyright 2026 EmbeddedOS Contributors. MIT License.*
