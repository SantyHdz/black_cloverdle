<script lang="ts">
  import { onMount } from 'svelte';
  import { fade, slide, scale } from 'svelte/transition';
  import './page.css';
  import GuessInput from '$lib/components/GuessInput.svelte';
  import GuessRow from '$lib/components/GuessRow.svelte';

  // ── Estado del juego ──────────────────────────────────────────────────────
  let guesses = $state<any[]>([]);
  let gameOver = $state(false);
  let won = $state(false);
  let totalCharacters = $state(0);
  let errorMsg = $state('');
  let submitError = $state('');
  let loading = $state(false);
  let showLegend = $state(false);

  // ── Al montar: obtener metadata del reto diario ───────────────────────────
  onMount(async () => {
    try {
      const res  = await fetch('/api/daily');
      const data = await res.json();
      totalCharacters = data.total_characters ?? 0;
    } catch {
      errorMsg = 'No se pudo conectar con el servidor. ¿Está corriendo el backend?';
    }
  });

  // ── Manejar un intento ────────────────────────────────────────────────────
  async function handleGuess(e: CustomEvent<string>) {
    if (gameOver || loading) return;
    submitError = '';
    loading = true;

    const nombre = e.detail.trim();

    try {
      const res  = await fetch('/api/guess', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ nombre }),
      });
      const data = await res.json();

      if (!data.found) {
        submitError = `"${nombre}" no existe en la base de datos. Verifica el nombre.`;
        return;
      }

      guesses = [...guesses, data.comparison];

      if (data.is_correct) {
        gameOver = true;
        won = true;
      }
    } catch {
      submitError = 'Error al comunicarse con el servidor.';
    } finally {
      loading = false;
    }
  }

  // ── Reiniciar (solo modo debug / desarrollo) ──────────────────────────────
  function resetGame() {
    guesses    = [];
    gameOver   = false;
    won        = false;
    submitError = '';
  }

</script>

<svelte:head>
  <title>BlackCloverdle — Adivina el Personaje</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="" />
  <link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700;900&family=Cinzel:wght@400;600;700&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet" />
</svelte:head>

<!-- ══════════════════════════════════════════════════════
     FONDO: partículas + textura de pergamino mágico
═══════════════════════════════════════════════════════ -->
<div class="bg-layer" aria-hidden="true">
  <div class="bg-noise"></div>
  <div class="bg-vignette"></div>
  {#each Array(18) as _, i}
    <span class="particle" style="
      left: {5 + (i * 5.3) % 90}%;
      top:  {10 + (i * 7.1) % 80}%;
      animation-delay: {(i * 0.4) % 5}s;
      animation-duration: {3 + (i * 0.3) % 4}s;
      font-size: {0.5 + (i * 0.07) % 0.8}rem;
      opacity: {0.03 + (i * 0.012) % 0.08};
    ">{['✦','◆','❖','✧','◇','⬡'][i % 6]}</span>
  {/each}
</div>

<!-- ══════════════════════════════════════════════════════
     CONTENIDO PRINCIPAL
═══════════════════════════════════════════════════════ -->
<main class="main">

  <!-- ── Cabecera ─────────────────────────────────────────────────────────── -->
  <header class="header" in:slide={{ duration: 600, axis: 'y' }}>
    <div class="header-rune left" aria-hidden="true" in:fade={{ duration: 800, delay: 200 }}>❖</div>

    <div class="header-center">
      <p class="header-eyebrow" in:fade={{ duration: 400, delay: 100 }}>El reto de hoy</p>
      <h1 class="header-title" in:scale={{ duration: 500, delay: 150 }}>
        <span class="title-black">BLACK</span>
		<span class="title-symbol">❁</span>
        <span class="title-clover">CLOVER</span>
        <span class="title-dle">DLE</span>
      </h1>
      <p class="header-sub" in:fade={{ duration: 400, delay: 300 }}>
        Adivina el personaje de hoy
        {#if totalCharacters > 0}
          · <span class="char-count">{totalCharacters} personajes disponibles</span>
        {/if}
      </p>
    </div>

    <div class="header-rune right" aria-hidden="true" in:fade={{ duration: 800, delay: 400 }}>❖</div>
  </header>

  <!-- ── Divisor decorativo ─────────────────────────────────────────────────── -->
  <div class="divider" aria-hidden="true" in:slide={{ duration: 500, axis: 'x', delay: 400 }}>
    <span class="divider-line"></span>
    <span class="divider-glyph">✦</span>
    <span class="divider-line"></span>
  </div>

  <!-- ── Error de conexión ──────────────────────────────────────────────────── -->
  {#if errorMsg}
    <div class="alert alert--error" in:slide={{ duration: 300, axis: 'y' }}>
      <span>⚠</span> {errorMsg}
    </div>
  {/if}

  <!-- ── Input de adivinanza (arriba) ───────────────────────────────────────── -->
  {#if !gameOver}
    <div class="input-area" in:fade={{ duration: 500, delay: 500 }}>
      {#if submitError}
        <p class="submit-error" role="alert" in:slide={{ duration: 200, axis: 'y' }}>{submitError}</p>
      {/if}
      <GuessInput
        disabled={loading || gameOver}
        placeholder="Escribe el nombre del personaje..."
        on:guess={handleGuess}
      />
      {#if loading}
        <p class="loading-hint" in:fade={{ duration: 300 }}>Consultando el grimorio...</p>
      {/if}
    </div>
  {/if}

  <!-- ══ ÁREA DEL JUEGO ══════════════════════════════════════════════════════ -->
  <section class="game-area">

    <!-- Cabecera de columnas -->
    {#if guesses.length > 0}
      <div class="col-header-row">
        <div class="attempt-spacer"></div>
        {#each ['Nombre','Género','Atributos','Raza','Altura','Reino','Orden','Magia','Arco'] as col}
          <div class="col-head">{col}</div>
        {/each}
      </div>
    {/if}

    <!-- Filas de intentos -->
    <div class="guesses-list">
      {#each guesses as comparison, i}
        <GuessRow {comparison} attemptNumber={i + 1} />
      {/each}
    </div>

    <!-- ── Pantalla de fin de juego ──────────────────────────────────────── -->
    {#if gameOver}
      <div class="endgame" class:endgame--win={won} class:endgame--lose={!won} in:scale={{ duration: 600, delay: 200 }}>
        {#if won}
          <div class="endgame-icon">✦</div>
          <h2 class="endgame-title" in:fade={{ duration: 400, delay: 400 }}>¡Personaje Descubierto!</h2>
          <p class="endgame-msg" in:fade={{ duration: 400, delay: 500 }}>
            Lo lograste en <strong>{guesses.length}</strong>
            {guesses.length === 1 ? 'intento' : 'intentos'}.
          </p>
        {:else}
          <div class="endgame-icon" style="color:#a83232" in:fade={{ duration: 300 }}>☠</div>
          <h2 class="endgame-title" style="color:#c45555" in:fade={{ duration: 400, delay: 200 }}>El mago escapó...</h2>
          <p class="endgame-msg" in:fade={{ duration: 400, delay: 300 }}>¡Sigue intentando! El personaje era:</p>
        {/if}
      </div>
    {/if}

  </section>

  <!-- ── Leyenda de colores ─────────────────────────────────────────────────── -->
	<div class="legend-wrapper">
		<button class="col-head" on:click={() =>
			(showLegend = !showLegend)}>
			<span class="col-head-label">Indicadores de color</span>
			<span class="col-head-arrow" class:open={"showLegend"}>▼</span>
		</button>

		{#if showLegend}
		<div class="legend" role="list">
			<div class="legend-item" role="listitem">
				<div class="legend-swatch swatch--correct"></div>
				<div class="legend-item-text">
					<strong>Correcto</strong>
					<span>El valor coincide exactamente</span>
				</div>
			</div>
			<div class="legend-item" role="listitem">
				<div class="legend-swatch swatch--partial"></div>
				<div class="legend-item-text">
					<strong>Parcial</strong>
					<span>Comparte al menos un valor (listas)</span>
				</div>
			</div>
			<div class="legend-item" role="listitem">
				<div class="legend-swatch swatch--incorrect"></div>
				<div class="legend-item-text">
					<strong>Incorrecto</strong>
					<span>No hay coincidencia</span>
				</div>
			</div>
			<div class="legend-item" role="listitem">
				<div class="legend-swatch swatch--directional"></div>
				<div class="legend-item-text">
					<strong>↑ / ↓</strong>
					<span>El objetivo es mayor/menor o anterior/posterior</span>
				</div>
			</div>
		</div>
		{/if}
	</div>

</main>