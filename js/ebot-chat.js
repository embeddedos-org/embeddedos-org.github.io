/* EmbeddedOS eBot — AI Chat Assistant */
(function () {
  'use strict';

  var KB = [
    { q: ['what is embeddedos', 'what is eos', 'about embeddedos', 'tell me about'], a: 'EmbeddedOS is a modular, multi-platform operating system designed for every device — from tiny microcontrollers to desktops, TVs, and spacecraft. It features 14 core components, supports 52+ platforms across 12 architectures (ARM, RISC-V, x86, Xtensa, etc.), and includes AI inference, secure IPC, OTA updates, a browser engine, database, office suite, and 60+ apps.' },
    { q: ['get started', 'how to start', 'quickstart', 'install', 'setup'], a: 'Getting started is easy!\n\n1. **Simulator (no hardware):** `pip install eosim && eosim run stm32f4`\n2. **Raspberry Pi:** Flash the EoS image to an SD card\n3. **STM32:** `ebuild init my-project --board stm32f4 && ebuild build && ebuild flash`\n4. **Apps:** `cmake -B build -DEAPPS_PORT=sdl2 && cmake --build build`\n\nVisit our [Getting Started](getting-started.html) page for detailed guides!' },
    { q: ['how many platforms', 'supported platforms', 'supported boards', 'hardware support'], a: 'EmbeddedOS supports **52+ platforms** across 12 architectures:\n- **ARM Cortex-M:** STM32F4, STM32H7, nRF52840, nRF5340, K64F, S32K344\n- **ARM Cortex-A:** Raspberry Pi 4/5, i.MX 8M, Jetson Orin, BeagleBone\n- **RISC-V:** ESP32-C3, SiFive U74, GD32VF103\n- **Others:** ESP32 (Xtensa), x86_64, PowerPC, MIPS, ARC\n\nCheck [Hardware Lab](hardware-lab.html) for details!' },
    { q: ['kernel', 'rtos', 'eos kernel', 'real-time'], a: 'The **EoS Kernel** is the core RTOS framework with:\n- 41 product category profiles (automotive, medical, aerospace, IoT, etc.)\n- 33 HAL peripheral drivers\n- SMP/AMP multicore support\n- Power management, networking (TCP/HTTP/MQTT)\n- Crypto (SHA-256, AES, RSA/ECC)\n- OTA updates, sensor framework, motor control\n\nSee [EoS Docs](docs/eos.html)' },
    { q: ['bootloader', 'eboot', 'secure boot', 'firmware update'], a: '**eBoot** is a production-grade bootloader supporting 24 board ports across 10 architectures. Features include:\n- Staged boot (stage-0 + stage-1)\n- A/B slots with automatic rollback\n- Secure boot chain with cryptographic verification\n- Stream-based firmware updates\n- SMP/AMP/lockstep multicore boot\n\nSee [eBoot Docs](docs/eboot.html)' },
    { q: ['ai', 'eai', 'machine learning', 'llm', 'inference'], a: '**EAI** is our embedded AI framework with two tiers:\n- **EAI-Min:** 50KB RAM, for MCUs — basic inference\n- **EAI-Framework:** Enterprise — 12 curated LLMs (TinyLlama to Qwen2.5 7B)\n- ReAct agents with tool calling\n- LoRA fine-tuning\n- Federated learning\n- 8-layer security\n- Power-aware inference\n\nSee [EAI Docs](docs/eai.html)' },
    { q: ['build', 'ebuild', 'compile', 'cmake', 'toolchain'], a: '**ebuild** is the unified build system with 18 CLI commands:\n- Cross-compilation (CMake/Make/Meson/Cargo/Kbuild)\n- Hardware schematic analysis (KiCad/YAML)\n- SDK generation\n- Package management with YAML recipes\n- 6 project templates\n- Deployable OS images for 14+ targets\n\nSee [ebuild Docs](docs/ebuild.html)' },
    { q: ['ipc', 'eipc', 'inter-process', 'communication'], a: '**EIPC** provides secure, real-time IPC with Go & C SDKs:\n- Pluggable transports (TCP, Unix sockets, shared memory, Windows pipes)\n- HMAC-SHA256 integrity\n- Capability-based auth\n- Pub/sub broker\n- Policy engine with replay protection\n\nSee [EIPC Docs](docs/eipc.html)' },
    { q: ['simulator', 'eosim', 'emulator', 'qemu', 'simulation'], a: '**EoSim** is the simulation platform supporting 52+ platforms:\n- Native Python engine\n- Renode integration\n- QEMU binary emulation\n- HIL (Hardware-in-Loop) bridge\n- GPIO/UART/Timer register maps\n- GUI dashboard with 3D renderers\n- Cluster simulation\n\nSee [EoSim Docs](docs/eosim.html)' },
    { q: ['browser', 'ebrowser', 'html', 'web engine'], a: '**eBrowser** is a lightweight web browser engine for embedded/IoT:\n- HTML5/CSS rendering\n- Optional JavaScript engine\n- Modular architecture (rendering/network/input layers)\n- Platform abstraction for Linux/RTOS/bare-metal\n- 130+ test cases\n\nSee [eBrowser Docs](docs/ebrowser.html)' },
    { q: ['database', 'edb', 'sql', 'nosql'], a: '**eDB** is a unified multi-model database:\n- SQL + Document/NoSQL + Key-Value in one engine\n- Built on SQLite (zero dependencies)\n- REST API via FastAPI\n- JWT auth, RBAC, AES-256 encryption\n- Full-text search, graph queries\n- eBot AI natural language interface\n\nSee [eDB Docs](docs/edb.html)' },
    { q: ['office', 'eoffice', 'docs', 'spreadsheet', 'slides'], a: '**eOffice** is a complete office suite with 11 apps:\neDocs, eSheets, eSlides, eNotes, eMail, eDB, eDrive, eConnect, eForms, eSway, and ePlanner. All powered by **eBot** AI assistant for text rewriting, formula suggestions, and semantic search.\n\nSee [eOffice Docs](docs/eoffice.html)' },
    { q: ['apps', 'eapps', 'app store', 'applications', 'mobile'], a: '**eApps** is our unified app store with **60+ apps** across all platforms:\n- 11 browser/editor extensions\n- 4 desktop apps (eOffice, EoStudio, EoSim, eBrowser)\n- 5 mobile apps (eRide, eSocial, eTrack, eTravel, eWallet)\n- 40+ native LVGL apps\n- Automated CI/CD builds\n\nVisit the [App Store](https://embeddedos-org.github.io/eApps/)!' },
    { q: ['neural', 'eni', 'brain', 'bci', 'neuralink'], a: '**ENI** (Embedded Neural Interface) is for brain-computer interfaces:\n- Neuralink 1024-channel adapter at 30kHz\n- EEG headset provider\n- DSP (FIR/IIR/FFT)\n- Lightweight neural network\n- Intent decoder\n- Neurofeedback & stimulation with safety interlocks\n\nSee [ENI Docs](docs/eni.html)' },
    { q: ['studio', 'eostudio', 'design', 'editor', 'ide'], a: '**EoStudio** is a unified design suite with 12 editors:\n3D modeler, CAD designer, image editor, game editor, UI/UX designer, UML modeler, simulation editor, database designer, PCB editor, and IDE. Includes 30+ code generators and LLM-powered AI.\n\nSee [EoStudio Docs](docs/eostudio.html)' },
    { q: ['book', 'books', 'pdf', 'guide', 'documentation download'], a: 'We have **16 official books** covering the entire ecosystem:\n- The Complete Guide (36 chapters, 12,500+ lines)\n- Individual product books for each repository\n- All free to download as PDF (CC BY-SA 4.0)\n\nVisit [Books](books.html) or download the [Complete Guide PDF](https://github.com/embeddedos-org/eos/releases/download/v0.2.0-book/embeddedos-complete-guide.pdf)' },
    { q: ['license', 'open source', 'mit'], a: 'EmbeddedOS is **100% open source** under the **MIT License**. All code, documentation, and books are freely available. Contributions are welcome!' },
    { q: ['automotive', 'car', 'vehicle', 'can bus'], a: 'EmbeddedOS supports automotive with the `automotive` profile:\n- CAN/CAN-FD bus support\n- ISO 26262 safety compliance\n- Sensor fusion\n- Motor control, watchdog\n- Supported boards: S32K344, TDA4VM\n\nPerfect for ECUs, ADAS, and EV battery management.' },
    { q: ['security', 'crypto', 'encryption', 'secure'], a: 'EmbeddedOS is **secure by default**:\n- Secure boot chain\n- SHA-256/AES/RSA/ECC crypto\n- A/B firmware updates with rollback\n- mTLS IPC\n- JWT auth, RBAC\n- 8-layer AI security\n- Tamper-resistant audit logs\n- FIPS 140-3 compliance' },
    { q: ['contribute', 'contributing', 'help', 'community'], a: 'We welcome contributions! Here\'s how:\n1. Fork the repo on [GitHub](https://github.com/embeddedos-org)\n2. Create a feature branch\n3. Submit a Pull Request\n\nCheck [CONTRIBUTING.md](https://github.com/embeddedos-org/eos/blob/main/CONTRIBUTING.md) for guidelines.\n\nJoin [Discussions](https://github.com/embeddedos-org/eos/discussions) to connect with the community.' },
    { q: ['hello', 'hi', 'hey', 'greetings'], a: 'Hello! I\'m **eBot**, the EmbeddedOS AI assistant. I can help you with:\n- Getting started with EmbeddedOS\n- Understanding components (EoS, eBoot, EAI, etc.)\n- Finding documentation\n- Hardware compatibility\n- Use cases & architecture\n\nWhat would you like to know?' },
    { q: ['thanks', 'thank you', 'thx'], a: 'You\'re welcome! If you have more questions, I\'m here to help. Happy building with EmbeddedOS!' }
  ];

  var FALLBACK = 'I\'m not sure about that specific topic. Here are some things I can help with:\n- **Getting started** — setup and installation\n- **Components** — EoS, eBoot, EAI, EIPC, etc.\n- **Hardware** — supported boards and platforms\n- **Architecture** — how everything fits together\n\nOr try our [Documentation](docs/index.html) and [Search](/) for more!';

  function findAnswer(msg) {
    var lower = msg.toLowerCase().trim();
    if (lower.length < 2) return FALLBACK;

    var best = null, bestScore = 0;
    for (var i = 0; i < KB.length; i++) {
      var entry = KB[i];
      for (var j = 0; j < entry.q.length; j++) {
        var pattern = entry.q[j];
        if (lower.includes(pattern)) {
          var score = pattern.length / lower.length + pattern.length * 0.1;
          if (score > bestScore) { bestScore = score; best = entry; }
        }
      }
    }
    // token matching fallback
    if (!best) {
      var tokens = lower.split(/\s+/).filter(function (t) { return t.length > 2; });
      for (var i = 0; i < KB.length; i++) {
        var entry = KB[i];
        var allQ = entry.q.join(' ');
        var matched = tokens.filter(function (t) { return allQ.includes(t); });
        var score = matched.length / tokens.length;
        if (score > bestScore && score > 0.3) { bestScore = score; best = entry; }
      }
    }
    return best ? best.a : FALLBACK;
  }

  function mdToHtml(md) {
    return md
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" style="color:var(--cyan)">$1</a>')
      .replace(/\n/g, '<br>');
  }

  function createWidget() {
    // Floating button
    var fab = document.createElement('button');
    fab.id = 'ebot-fab';
    fab.setAttribute('aria-label', 'Open eBot AI Assistant');
    fab.innerHTML = '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>';
    document.body.appendChild(fab);

    // Chat panel
    var panel = document.createElement('div');
    panel.id = 'ebot-panel';
    panel.hidden = true;
    panel.innerHTML =
      '<div class="ebot-header">' +
        '<div class="ebot-title"><span class="ebot-dot"></span> eBot AI Assistant</div>' +
        '<button class="ebot-close" aria-label="Close chat">&times;</button>' +
      '</div>' +
      '<div class="ebot-messages" id="ebot-messages">' +
        '<div class="ebot-msg ebot-bot">' +
          '<div class="ebot-bubble">Hi! I\'m <strong>eBot</strong>, the EmbeddedOS AI assistant. Ask me anything about EmbeddedOS — components, getting started, hardware support, or architecture!</div>' +
        '</div>' +
      '</div>' +
      '<div class="ebot-suggestions" id="ebot-suggestions">' +
        '<button class="ebot-suggest-btn" data-q="What is EmbeddedOS?">What is EmbeddedOS?</button>' +
        '<button class="ebot-suggest-btn" data-q="How do I get started?">Get Started</button>' +
        '<button class="ebot-suggest-btn" data-q="What platforms are supported?">Platforms</button>' +
        '<button class="ebot-suggest-btn" data-q="Tell me about the AI framework">AI/ML</button>' +
      '</div>' +
      '<form class="ebot-input-area" id="ebot-form">' +
        '<input type="text" class="ebot-input" id="ebot-input" placeholder="Ask about EmbeddedOS..." autocomplete="off">' +
        '<button type="submit" class="ebot-send" aria-label="Send">&#10148;</button>' +
      '</form>';
    document.body.appendChild(panel);

    // Events
    fab.addEventListener('click', function () { panel.hidden = !panel.hidden; fab.classList.toggle('active'); if (!panel.hidden) document.getElementById('ebot-input').focus(); });
    panel.querySelector('.ebot-close').addEventListener('click', function () { panel.hidden = true; fab.classList.remove('active'); });

    var form = document.getElementById('ebot-form');
    var input = document.getElementById('ebot-input');
    var messages = document.getElementById('ebot-messages');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var text = input.value.trim();
      if (!text) return;
      addMessage(text, 'user');
      input.value = '';
      // Hide suggestions after first message
      var sug = document.getElementById('ebot-suggestions');
      if (sug) sug.style.display = 'none';
      // Simulate typing
      var typing = addMessage('<span class="ebot-typing">Thinking...</span>', 'bot');
      setTimeout(function () {
        var answer = findAnswer(text);
        typing.querySelector('.ebot-bubble').innerHTML = mdToHtml(answer);
        messages.scrollTop = messages.scrollHeight;
      }, 400 + Math.random() * 400);
    });

    // Suggestion buttons
    panel.querySelectorAll('.ebot-suggest-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        input.value = btn.dataset.q;
        form.dispatchEvent(new Event('submit'));
      });
    });
  }

  function addMessage(html, role) {
    var messages = document.getElementById('ebot-messages');
    var div = document.createElement('div');
    div.className = 'ebot-msg ebot-' + role;
    div.innerHTML = '<div class="ebot-bubble">' + html + '</div>';
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
    return div;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createWidget);
  } else {
    createWidget();
  }
})();
