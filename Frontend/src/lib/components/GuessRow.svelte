<script lang="ts">
	import FlipCard from './FlipCard.svelte';

	/**
	 * comparison — el objeto que devuelve el backend para un intento:
	 * {
	 *   nombre: { value, result },
	 *   genero: { value, result },
	 *   atributos: { value, result },
	 *   raza: { value, result },
	 *   altura: { value, result },
	 *   reino: { value, result },
	 *   orden: { value, result },
	 *   tipo_magia: { value, result },
	 *   arco: { value, result },
	 *   is_correct: boolean
	 * }
	 */

	// Props usando runes
	const { comparison, attemptNumber = 1 } = $props<{
		comparison: Record<string, any>;
		attemptNumber?: number;
	}>();

	// Definición de columnas en el orden visual
	const COLUMNS: { key: string; label: string }[] = [
		{ key: 'nombre', label: 'Nombre' },
		{ key: 'genero', label: 'Género' },
		{ key: 'atributos', label: 'Atributos' },
		{ key: 'raza', label: 'Raza' },
		{ key: 'altura', label: 'Altura' },
		{ key: 'reino', label: 'Reino' },
		{ key: 'orden', label: 'Orden' },
		{ key: 'tipo_magia', label: 'Magia' },
		{ key: 'arco', label: 'Arco' }
	];

	// Delay escalonado por tarjeta (ms)
	const BASE_DELAY = 80;
	const ATTEMPT_EXTRA = 0;
</script>

<div class="guess-row" class:guess-row--win={comparison?.is_correct}>
	<!-- Número de intento -->
	<div class="attempt-badge">
		<span>{attemptNumber}</span>
	</div>

	<!-- Tarjetas -->
	<div class="cards-grid">
		{#each COLUMNS as col, i}
			{@const field = comparison?.[col.key]}
			<FlipCard
				value={field?.value ?? '—'}
				result={field?.result ?? 'incorrect'}
				label={col.label}
				delay={ATTEMPT_EXTRA + i * BASE_DELAY}
			/>
		{/each}
	</div>

	{#if comparison?.is_correct}
		<div class="win-banner">
			<span class="win-rune">✦</span>
			¡Correcto!
			<span class="win-rune">✦</span>
		</div>
	{/if}
</div>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&display=swap');

  /* ── Fila completa ── */
  .guess-row {
    display: flex;
    align-items: center;
    gap: 10px;
    width: 100%;
    padding: 6px 0;
    position: relative;
    animation: row-in 0.3s ease both;
  }

  @keyframes row-in {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  /* Fila ganadora: sutil halo */
  .guess-row--win {
    filter: drop-shadow(0 0 12px rgba(46, 165, 85, 0.5));
  }

  /* ── Número de intento ── */
  .attempt-badge {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #1c2130;
    border: 1px solid #30363d;
    flex-shrink: 0;
  }

  .attempt-badge span {
    font-family: 'Cinzel', serif;
    font-size: 0.7rem;
    font-weight: 700;
    color: #8b949e;
  }

  /* ── Grid de tarjetas ── */
  .cards-grid {
    display: grid;
    grid-template-columns: repeat(9, 1fr);
    gap: 6px;
    flex: 1;
    min-width: 0;
  }

  /* Responsive: en móvil 3 columnas */
  @media (max-width: 700px) {
    .cards-grid {
      grid-template-columns: repeat(3, 1fr);
    }
  }

  /* ── Banner de victoria ── */
  .win-banner {
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'Cinzel', serif;
    font-size: 0.85rem;
    font-weight: 700;
    color: #2ea555;
    white-space: nowrap;
    text-shadow: 0 0 10px rgba(46, 165, 85, 0.6);
    animation: banner-in 0.6s ease 0.8s both;
  }

  @keyframes banner-in {
    from { opacity: 0; transform: scale(0.8); }
    to   { opacity: 1; transform: scale(1); }
  }

  .win-rune {
    animation: spin-rune 3s linear infinite;
    display: inline-block;
    color: #c9a84c;
  }

  @keyframes spin-rune {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
  }
</style>