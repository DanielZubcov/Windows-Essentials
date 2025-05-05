# Win Setup Wizard

Instalador completo pós-formatação para Windows 10/11.

## Funcionalidades

- Instala DirectX, .NET Framework, Visual C++ Redistributables (e outros, só falta implementar)
- Detecta automaticamente drivers de vídeo (NVIDIA, AMD, Intel)
- Interface amigável estilo "wizard" (ainda precisa ser implementado)
- Suporte offline (instaladores embutidos, com exceção dos drivers de video)

## Requisitos

- Windows 10 ou superior

## Como usar (atualmente)

1. Baixe o zip do repo
2. extraia tudo numa pasta
3. instale via PIP os [requisitos](required_libs.txt)
4. Dentro da pasta que contém a [main](src/main.py) execute no terminal
   ```terminal
   python main.py
   ```

## Como usar (Versão final)

1. Baixe o executável aqui [em breve]
2. Execute e siga os passos da interface

## Licença

MIT - veja `LICENSE`
