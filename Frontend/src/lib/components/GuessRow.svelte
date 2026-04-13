<script lang="ts">
	import FlipCard from './FlipCard.svelte';
	import './GuessRow.css';

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