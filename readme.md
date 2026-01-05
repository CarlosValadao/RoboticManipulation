# 🤖 Projeto NXT: Automação Logística e Engenharia Robótica (NXC) 🚀

Este projeto representa a convergência entre a **Engenharia de Computação** e a **Robótica de Precisão**. Desenvolvemos não apenas o firmware de alto desempenho em linguagem **NXC (Not eXactly C)**, mas também toda a **concepção e montagem da estrutura física do robô** 🏗️, otimizada para desafios logísticos autônomos.

---

## 🏛️ Arquitetura do Sistema e Design de Hardware ⚙️

O robô foi projetado sob uma perspectiva sistêmica integral, onde o design mecânico e a lógica de software operam em perfeita simbiose para garantir a máxima eficiência em ambiente de missão crítica.

### 🏗️ Estrutura Física Customizada

* **Engenharia Mecânica:** Todo o chassi e o sistema de tração foram desenvolvidos por nossa equipe, focando em estabilidade e precisão de manobra.
* **Atuadores e Garra:** Projeto e montagem de uma garra motorizada para manipulação de carga com sensores de fim de curso integrados.

### 🛰️ Navegação e Odometria de Alta Fidelidade

O robô utiliza um sistema de **odometria avançada** para estimar sua posição global ($X$ e $Y$) e orientação em tempo real.

* **Cálculo de Deslocamento:** Implementação manual de funções trigonométricas para inferir a trajetória com base nos contadores de rotação dos motores 📐.
* **Bússola Virtual:** Gerenciamento de estado para manter a orientação do robô (Norte, Sul, Leste, Oeste) durante as manobras 🧭.

### 🎮 Inteligência Sensorial

* **3 Motores**: Movimentação do robô e Garra
* **Sensores Ultrassônicos:** Detecção de obstáculos e medição de distância em tempo real para evitar colisões 🔊.
* **Visão de Cor:** Identificação precisa de superfícies (preto para limites, prata para bases e zonas de carga) 🌈.
* **Sensores de Toque:** Feedback tátil para calibração de garra e detecção física de barreiras ⚡.

---

## 🛠️ Diferenciais Técnicos e Inovação 🔬

* **Multitarefa e Concorrência:** Uso de **Tasks** simultâneas e **Mutexes** para garantir a integridade dos dados de telemetria e evitar condições de corrida 🧵.
* **Telemetria via Bluetooth:** O robô atua como um nó inteligente, enviando coordenadas e status de operação para um supervisor remoto em tempo real 📡.
* **Algoritmos de Busca Dinâmica:** Lógica sofisticada para localização autônoma de entradas de estoque e bancadas, adaptando-se a variações no ambiente 🔍.

---

## 📂 Fluxo Operacional Autônomo 🔄

A missão é executada através de uma máquina de estados rigorosa:

1. **Aguardar:** Stand-by para recepção de comandos via Bluetooth ⏳.
2. **Navegação de Saída:** Manobras de evasão da base inicial 🏃.
3. **Logística de Carga:** Localização do estoque, captura e transporte seguro do objeto 📦.
4. **Entrega de Precisão:** Depósito da carga na bancada designada com reorientação automática 📍.
5. **Retorno Triunfal:** Navegação de volta à base e finalização da operação ✅.

---

## 💻 Tecnologias e Ferramentas 🛠️

* **Firmware:** NXC (Not eXactly C).
* **Hardware:** Lego Mindstorms NXT Intelligent Brick + Estrutura customizada.
* **Protocolos:** RFCOMM (Bluetooth) para comunicação entre robôs e supervisórios.
* **Matemática:** Geometria Analítica e Trigonometria aplicada à robótica móvel.

---
*"A engenharia é o palco onde a teoria encontra a matéria para criar a autonomia."* 🧠✨
