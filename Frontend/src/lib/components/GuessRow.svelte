<script lang="ts">
	import FlipCard from './FlipCard.svelte';
import { slide, fade, scale } from 'svelte/transition';
import './GuessRow.css';

const { comparison, attemptNumber = 1 } = $props<{
    comparison: Record<string, any>;
    attemptNumber?: number;
}>();

const COLUMNS: { key: string; label: string }[] = [
    { key: 'nombre',     label: 'Nombre'   },
    { key: 'genero',     label: 'Género'   },
    { key: 'atributos',  label: 'Atributos'},
    { key: 'raza',       label: 'Raza'     },
    { key: 'altura',     label: 'Altura'   },
    { key: 'reino',      label: 'Reino'    },
    { key: 'orden',      label: 'Orden'    },
    { key: 'tipo_magia', label: 'Magia'    },
    { key: 'arco',       label: 'Arco'     }
];

const BASE_DELAY = 80;
const ATTEMPT_EXTRA = 0;

function getCharacterImage(name: string) {
    if (!name) return '';
    return `/images/characters/${name.toLowerCase().replaceAll(' ', '_')}.webp`;
}
</script>

<div
	class="guess-row"
	class:guess-row--win={comparison?.is_correct}
	in:slide={{ duration: 400, axis: 'y' }}
>

	<!-- Número intento -->
	<div
		class="attempt-badge"
		in:fade={{ duration: 300, delay: 100 }}
	>
		<span>{attemptNumber}</span>
	</div>

	<!-- Tarjetas -->
	<div class="cards-grid">

		{#each COLUMNS as col, i}

	{@const field = comparison?.[col.key]}

	{#if col.key === 'nombre'}

		<!-- 🖼️ Tarjeta con imagen -->
		<FlipCard
			value={getCharacterImage(field?.value)}
			result={field?.result ?? 'incorrect'}
			label={field?.value}
			delay={ATTEMPT_EXTRA + i * BASE_DELAY}
			isImage={true}
		/>

	{:else}

		<!-- Tarjetas normales -->
		<FlipCard
			value={field?.value ?? '—'}
			result={field?.result ?? 'incorrect'}
			label={col.label}
			delay={ATTEMPT_EXTRA + i * BASE_DELAY}
		/>

	{/if}

{/each}



	</div>

	{#if comparison?.is_correct}

		<div
			class="win-banner"
			in:scale={{ duration: 500, delay: 600 }}
		>
			<span class="win-rune">✦</span>
			¡Correcto!
			<span class="win-rune">✦</span>
		</div>

	{/if}

</div>
