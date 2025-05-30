# Cálculos Numéricos em Go

Este repositório contém duas questões implementadas em Go:

1. Questão 3: Cálculo de derivadas e vetores de velocidade/aceleração
2. Questão 4: Integração numérica usando o método de Gauss-Legendre

## Pré-requisitos

- Go instalado (versão 1.16 ou superior)
- Para verificar a instalação do Go, execute:
  ```bash
  go version
  ```

## Como Executar

### Questão 3
Para executar o programa que calcula as derivadas e vetores de velocidade/aceleração:

```bash
go run questao_3.go
```

Este programa irá calcular e exibir:
- Velocidade (er, eθ) em m/s
- Aceleração (er, eθ) em m/s²

### Questão 4
Para executar o programa que calcula a integração numérica:

```bash
go run questao_4.go
```

Este programa irá calcular e exibir:
- O valor aproximado de M no intervalo [2, 8] em mg

## Resultados Esperados

### Questão 3
O programa mostrará os resultados para t = 206s, incluindo os vetores de velocidade e aceleração em coordenadas polares.

### Questão 4
O programa mostrará o valor aproximado de M, que deve ser próximo a 322.3562 mg.

## Estrutura do Código

- `questao_3.go`: Implementa cálculos de derivadas usando diferenças finitas
- `questao_4.go`: Implementa integração numérica usando o método de Gauss-Legendre
