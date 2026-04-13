<script lang="ts">
  import { onMount } from 'svelte';
  import './FlipCard.css';

  // Props usando runes
  const {
    value = '',
    result = 'incorrect',
    label = '',
    delay = 0
  }: {
    value?: string | string[];
    result?: 'correct' | 'partial' | 'incorrect' | 'higher' | 'lower';
    label?: string;
    delay?: number;
  } = $props();

  let flipped = $state(false);

  // Props derivadas para lógica de presentación
  const displayValue = $derived(
    Array.isArray(value)
      ? value.join(', ')
      : String(value ?? '—')
  );

  const colorClass = $derived(
    ({
      correct:   'card--correct',
      partial:   'card--partial',
      incorrect: 'card--incorrect',
      higher:    'card--directional',
      lower:     'card--directional',
    } as const)[result] ?? 'card--incorrect'
  );

  const arrow = $derived(
    result === 'higher' ? '↑' :
    result === 'lower'  ? '↓' :
    null
  );

  onMount(() => {
    const timer = setTimeout(() => {
      flipped = true;
    }, delay);

    return () => clearTimeout(timer);
  });
</script>

<div class="flip-wrapper" style="--flip-delay: {delay}ms">
  <div class="flip-inner" class:flipped={flipped}>
    <!-- Cara trasera -->
    <div class="flip-face flip-back">
      <div class="rune-symbol">✦</div>
    </div>

    <!-- Cara frontal -->
    <div class="flip-face flip-front {colorClass}">
      <span class="card-label">{label}</span>

      <span class="card-value">
        {displayValue}
        {#if arrow}
          <span class="card-arrow">{arrow}</span>
        {/if}
      </span>

      {#if result === 'correct'}
        <span class="card-glow"></span>
      {/if}
    </div>
  </div>
</div>