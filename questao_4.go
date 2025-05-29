package main

import (
	"fmt"
	"math"
)

// Pontos e pesos para n = 4 (Gauss-Legendre)
var pontos = []float64{-0.861136, -0.339981, 0.339981, 0.861136}
var pesos = []float64{0.347855, 0.652145, 0.652145, 0.347855}

// Q calcula a função Q(t)
func Q(t float64) float64 {
	return 9 + 4*math.Pow(math.Cos(0.4*t), 2)
}

// c calcula a função c(t)
func c(t float64) float64 {
	return 5*math.Exp(-0.5*t) + 2*math.Exp(0.15*t)
}

// f calcula a função f(t) = Q(t) * c(t)
func f(t float64) float64 {
	return Q(t) * c(t)
}

// gaussLegendreIntegralManual aplica a quadratura de Gauss-Legendre
func gaussLegendreIntegralManual(f func(float64) float64, a, b float64, pontos, pesos []float64) float64 {
	var soma float64
	for i := range pontos {
		// Transformação de variável: t = (b-a)/2 * x + (a+b)/2
		t := ((b-a)/2)*pontos[i] + (a+b)/2
		soma += pesos[i] * f(t)
	}
	return ((b - a) / 2) * soma
}

func main() {
	// Intervalo [a, b]
	a := 2.0
	b := 8.0

	// Cálculo final da massa M
	M := gaussLegendreIntegralManual(f, a, b, pontos, pesos)

	// Resultado
	fmt.Printf("Valor aproximado de M no intervalo [2, 8]: %.4f mg\n", M)
}
