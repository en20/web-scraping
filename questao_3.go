package main

import (
	"fmt"
)

// derivadaCentral4Pontos calcula a primeira derivada usando diferença central O(h^4)
func derivadaCentral4Pontos(f []float64, h float64) float64 {
	return (f[0] - 8*f[1] + 8*f[3] - f[4]) / (12 * h)
}

// segundaDerivada5Pontos calcula a segunda derivada usando diferença central O(h^4)
func segundaDerivada5Pontos(f []float64, h float64) float64 {
	return (-f[0] + 16*f[1] - 30*f[2] + 16*f[3] - f[4]) / (12 * h * h)
}

// calcularDerivadas calcula as derivadas no ponto t[indexAlvo]
func calcularDerivadas(t, r, theta []float64, indexAlvo int, h float64) (float64, float64, float64, float64) {
	i := indexAlvo
	var dotR, ddotR, dotTheta, ddotTheta float64

	if i < 2 || i > len(t)-3 {
		// Usar O(h^2) nas bordas
		dotR = (r[i+1] - r[i-1]) / (2 * h)
		ddotR = (r[i+1] - 2*r[i] + r[i-1]) / (h * h)
		dotTheta = (theta[i+1] - theta[i-1]) / (2 * h)
		ddotTheta = (theta[i+1] - 2*theta[i] + theta[i-1]) / (h * h)
	} else {
		// Usar O(h^4) no centro
		dotR = derivadaCentral4Pontos([]float64{r[i-2], r[i-1], r[i], r[i+1], r[i+2]}, h)
		ddotR = segundaDerivada5Pontos([]float64{r[i-2], r[i-1], r[i], r[i+1], r[i+2]}, h)
		dotTheta = derivadaCentral4Pontos([]float64{theta[i-2], theta[i-1], theta[i], theta[i+1], theta[i+2]}, h)
		ddotTheta = segundaDerivada5Pontos([]float64{theta[i-2], theta[i-1], theta[i], theta[i+1], theta[i+2]}, h)
	}
	return dotR, ddotR, dotTheta, ddotTheta
}

func main() {
	// Dados
	t := []float64{200, 202, 204, 206, 208, 210}
	r := []float64{5120, 5370, 5560, 5800, 6030, 6240}
	theta := []float64{0.75, 0.72, 0.70, 0.68, 0.67, 0.66}

	// Ponto de interesse: t = 206 s (índice 3)
	dotR, ddotR, dotTheta, ddotTheta := calcularDerivadas(t, r, theta, 3, 2)

	// Vetores velocidade e aceleração (polares)
	vR := dotR
	vTheta := r[3] * dotTheta
	aR := ddotR - r[3]*dotTheta*dotTheta
	aTheta := r[3]*ddotTheta + 2*dotR*dotTheta

	fmt.Println("--- Resultados em t = 206 s ---")
	fmt.Printf("Velocidade (er, eθ): [%.2f, %.2f] m/s\n", vR, vTheta)
	fmt.Printf("Aceleração (er, eθ): [%.2f, %.2f] m/s²\n", aR, aTheta)
}
