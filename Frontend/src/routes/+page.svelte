<script lang="ts">
  import { onMount } from 'svelte';
  import GuessInput from '$lib/components/GuessInput.svelte';
  import GuessRow from '$lib/components/GuessRow.svelte';

  // ── Estado del juego ──────────────────────────────────────────────────────
  // En Svelte 5, las variables de estado deben declararse con $state()
  let guesses = $state<any[]>([]);
  let gameOver = $state(false);
  let won = $state(false);
  let totalCharacters = $state(0);
  let errorMsg = $state('');
  let submitError = $state('');
  let loading = $state(false);
  let showLegend = $state(false);

  const MAX_GUESSES = 8;

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
      } else if (guesses.length >= MAX_GUESSES) {
        gameOver = true;
        won = false;
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

  // ── Intentos restantes ────────────────────────────────────────────────────
let remaining = $derived(MAX_GUESSES - guesses.length);
</script>

<svelte:head>
  <title>Black Cloverdle — Adivina el Personaje</title>
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
  <header class="header">
    <div class="header-rune left" aria-hidden="true">❖</div>

    <div class="header-center">
      <p class="header-eyebrow">El reto de hoy</p>
      <h1 class="header-title">
        <span class="title-black">BLACK</span>
        <span class="title-clover">CLOVER</span>
        <span class="title-dle">DLE</span>
      </h1>
      <p class="header-sub">
        Adivina el personaje de hoy en
        <strong>{MAX_GUESSES}</strong> intentos
        {#if totalCharacters > 0}
          · <span class="char-count">{totalCharacters} personajes disponibles</span>
        {/if}
      </p>
    </div>

    <div class="header-rune right" aria-hidden="true">❖</div>
  </header>

  <!-- ── Divisor decorativo ─────────────────────────────────────────────────── -->
  <div class="divider" aria-hidden="true">
    <span class="divider-line"></span>
    <span class="divider-glyph">✦</span>
    <span class="divider-line"></span>
  </div>

  <!-- ── Error de conexión ──────────────────────────────────────────────────── -->
  {#if errorMsg}
    <div class="alert alert--error">
      <span>⚠</span> {errorMsg}
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

    <!-- Placeholders de intentos vacíos -->
    {#if !gameOver && guesses.length < MAX_GUESSES}
      <div class="empty-slots">
        {#each Array(remaining) as _, i}
          <div class="empty-slot" style="opacity: {1 - i * 0.1}">
            <div class="attempt-spacer muted">{guesses.length + i + 1}</div>
            {#each Array(9) as _}
              <div class="empty-card"></div>
            {/each}
          </div>
        {/each}
      </div>
    {/if}

    <!-- ── Pantalla de fin de juego ──────────────────────────────────────── -->
    {#if gameOver}
      <div class="endgame" class:endgame--win={won} class:endgame--lose={!won}>
        {#if won}
          <div class="endgame-icon">✦</div>
          <h2 class="endgame-title">¡Grimorio Descubierto!</h2>
          <p class="endgame-msg">
            Lo lograste en <strong>{guesses.length}</strong>
            {guesses.length === 1 ? 'intento' : 'intentos'}.
          </p>
        {:else}
          <div class="endgame-icon" style="color:#a83232">☠</div>
          <h2 class="endgame-title" style="color:#c45555">El mago escapó...</h2>
          <p class="endgame-msg">Agotaste todos tus intentos. ¡Vuelve mañana!</p>
        {/if}

        <div class="endgame-actions">
          <!-- Botón solo visible en dev; en prod quitar -->
          <button class="btn-secondary" onclick={resetGame}>↺ Reiniciar (dev)</button>
        </div>
      </div>
    {/if}

  </section>

  <!-- ── Input de adivinanza ────────────────────────────────────────────────── -->
  {#if !gameOver}
    <div class="input-area">
      {#if submitError}
        <p class="submit-error" role="alert">{submitError}</p>
      {/if}
      <GuessInput
        disabled={loading || gameOver}
        placeholder="Escribe el nombre del personaje..."
        on:guess={handleGuess}
      />
      {#if loading}
        <p class="loading-hint">Consultando el grimorio...</p>
      {/if}
    </div>
  {/if}

  <!-- ── Leyenda de colores ─────────────────────────────────────────────────── -->
  <div class="legend-wrapper">
    <button class="legend-toggle" onclick={() => (showLegend = !showLegend)}>
      {showLegend ? '▲' : '▼'} Indicadores de color
    </button>

    {#if showLegend}
      <div class="legend" role="list">
        <div class="legend-item" role="listitem">
          <div class="legend-swatch swatch--correct"></div>
          <div>
            <strong>Correcto</strong>
            <span>El valor coincide exactamente</span>
          </div>
        </div>
        <div class="legend-item" role="listitem">
          <div class="legend-swatch swatch--partial"></div>
          <div>
            <strong>Parcial</strong>
            <span>Comparte al menos un valor (listas)</span>
          </div>
        </div>
        <div class="legend-item" role="listitem">
          <div class="legend-swatch swatch--incorrect"></div>
          <div>
            <strong>Incorrecto</strong>
            <span>No hay coincidencia</span>
          </div>
        </div>
        <div class="legend-item" role="listitem">
          <div class="legend-swatch swatch--directional"></div>
          <div>
            <strong>↑ / ↓</strong>
            <span>El objetivo es mayor o menor / anterior o posterior</span>
          </div>
        </div>
      </div>
    {/if}
  </div>

</main>

<!-- ══════════════════════════════════════════════════════
     ESTILOS GLOBALES DE PÁGINA
═══════════════════════════════════════════════════════ -->
<style>
  /* ── Reset & variables ── */
  :global(*, *::before, *::after) { box-sizing: border-box; margin: 0; padding: 0; }

  :global(body) {
    background: #070b0f;
    color: #e6edf3;
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* ── Fondo ── */
  .bg-layer {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
  }

  .bg-noise {
    position: absolute;
    inset: 0;
    background-image:
      radial-gradient(ellipse 80% 50% at 50% -10%, rgba(201,168,76,.07) 0%, transparent 60%),
      radial-gradient(ellipse 60% 40% at 20% 80%,  rgba(26,71,42,.12)  0%, transparent 55%);
  }

  .bg-vignette {
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,.7) 100%);
  }

  .particle {
    position: absolute;
    color: #c9a84c;
    animation: float-particle linear infinite;
    user-select: none;
  }

  @keyframes float-particle {
    0%   { transform: translateY(0) rotate(0deg); }
    50%  { transform: translateY(-18px) rotate(180deg); }
    100% { transform: translateY(0) rotate(360deg); }
  }

  /* ── Layout principal ── */
  .main {
    position: relative;
    z-index: 1;
    max-width: 1100px;
    margin: 0 auto;
    padding: 2.5rem 1.5rem 4rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2rem;
  }

  /* ── Cabecera ── */
  .header {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    text-align: center;
  }

  .header-center { flex: 1; }

  .header-rune {
    font-size: 1.6rem;
    color: #c9a84c;
    opacity: .25;
    animation: pulse-rune 3s ease-in-out infinite;
  }
  .header-rune.left  { animation-delay: 0s; }
  .header-rune.right { animation-delay: 1.5s; }

  @keyframes pulse-rune {
    0%,100% { opacity: .15; }
    50%      { opacity: .4; }
  }

  .header-eyebrow {
    font-family: 'Cinzel', serif;
    font-size: .7rem;
    letter-spacing: .25em;
    text-transform: uppercase;
    color: #c9a84c;
    opacity: .7;
    margin-bottom: .4rem;
  }

  .header-title {
    font-family: 'Cinzel Decorative', serif;
    line-height: 1;
    margin-bottom: .5rem;
  }

  .title-black  { font-size: clamp(1.6rem, 5vw, 3rem); font-weight: 900; color: #e6edf3; }
  .title-clover { font-size: clamp(1.6rem, 5vw, 3rem); font-weight: 900; color: #2ea555; letter-spacing: -.02em; }
  .title-dle    { font-size: clamp(1.1rem, 3.5vw, 2rem); font-weight: 400; color: #c9a84c; letter-spacing: .12em; }

  .header-sub {
    font-family: 'Crimson Pro', serif;
    font-size: .95rem;
    color: #8b949e;
  }

  .char-count { color: #5a7a5a; }

  /* ── Divisor ── */
  .divider {
    display: flex;
    align-items: center;
    gap: 12px;
    width: 100%;
    max-width: 600px;
  }

  .divider-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, #3a3010, transparent);
  }

  .divider-glyph {
    font-size: .7rem;
    color: #c9a84c;
    opacity: .5;
  }

  /* ── Alertas ── */
  .alert {
    width: 100%;
    max-width: 680px;
    padding: 12px 16px;
    border-radius: 8px;
    font-family: 'Crimson Pro', serif;
    font-size: .95rem;
    display: flex;
    gap: 8px;
    align-items: center;
  }

  .alert--error {
    background: #1a0808;
    border: 1px solid #6b1a1a;
    color: #f48080;
  }

  /* ── Área del juego ── */
  .game-area {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  /* Cabecera de columnas */
  .col-header-row {
    display: grid;
    grid-template-columns: 38px repeat(9, 1fr);
    gap: 6px;
    padding: 0 0 4px;
    animation: fade-in .4s ease both;
  }

  .attempt-spacer { width: 38px; flex-shrink: 0; }

  .col-head {
    font-family: 'Cinzel', serif;
    font-size: .6rem;
    text-transform: uppercase;
    letter-spacing: .1em;
    color: #3d3520;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Lista de intentos */
  .guesses-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  /* Slots vacíos */
  .empty-slots {
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin-top: 2px;
  }

  .empty-slot {
    display: grid;
    grid-template-columns: 38px repeat(9, 1fr);
    gap: 6px;
    align-items: center;
  }

  .attempt-spacer.muted {
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Cinzel', serif;
    font-size: .65rem;
    color: #2a2a2a;
  }

  .empty-card {
    height: 72px;
    border-radius: 8px;
    border: 1px dashed #1e1e1e;
    background: #0a0d10;
  }

  /* ── Fin de juego ── */
  .endgame {
    margin-top: 1.5rem;
    padding: 2rem;
    border-radius: 16px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    animation: endgame-in .5s cubic-bezier(.34,1.56,.64,1) both;
  }

  @keyframes endgame-in {
    from { opacity: 0; transform: scale(.9) translateY(20px); }
    to   { opacity: 1; transform: scale(1) translateY(0); }
  }

  .endgame--win  {
    background: linear-gradient(135deg, #061a0e 0%, #0f3d22 100%);
    border: 1px solid #2ea555;
    box-shadow: 0 0 40px rgba(46,165,85,.2);
  }

  .endgame--lose {
    background: linear-gradient(135deg, #150505 0%, #2a0a0a 100%);
    border: 1px solid #6b1a1a;
  }

  .endgame-icon {
    font-size: 2.5rem;
    color: #c9a84c;
    animation: bounce-icon .8s ease;
  }

  @keyframes bounce-icon {
    0%   { transform: scale(0) rotate(-20deg); }
    70%  { transform: scale(1.2) rotate(5deg); }
    100% { transform: scale(1) rotate(0deg); }
  }

  .endgame-title {
    font-family: 'Cinzel Decorative', serif;
    font-size: clamp(1.2rem, 3vw, 1.8rem);
    color: #c9a84c;
  }

  .endgame-msg {
    font-family: 'Crimson Pro', serif;
    font-size: 1.05rem;
    color: #8b949e;
  }

  .endgame-actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: .5rem;
  }

  .btn-secondary {
    padding: 10px 20px;
    background: transparent;
    border: 1px solid #30363d;
    border-radius: 8px;
    color: #8b949e;
    font-family: 'Cinzel', serif;
    font-size: .75rem;
    cursor: pointer;
    transition: border-color .2s, color .2s;
  }

  .btn-secondary:hover {
    border-color: #c9a84c;
    color: #c9a84c;
  }

  /* ── Input area ── */
  .input-area {
    width: 100%;
    max-width: 640px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    animation: fade-in .4s ease both;
  }

  .submit-error {
    font-family: 'Crimson Pro', serif;
    font-size: .9rem;
    color: #f48080;
    background: #1a0808;
    border: 1px solid #6b1a1a;
    border-radius: 6px;
    padding: 8px 14px;
    width: 100%;
    text-align: center;
    animation: shake .3s ease;
  }

  @keyframes shake {
    0%,100% { transform: translateX(0); }
    25%      { transform: translateX(-6px); }
    75%      { transform: translateX(6px); }
  }

  .loading-hint {
    font-family: 'Crimson Pro', serif;
    font-size: .85rem;
    color: #c9a84c;
    opacity: .7;
    animation: pulse-hint 1s ease-in-out infinite;
  }

  @keyframes pulse-hint {
    0%,100% { opacity: .4; }
    50%      { opacity: .9; }
  }

  /* ── Leyenda ── */
  .legend-wrapper {
    width: 100%;
    max-width: 680px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
  }

  .legend-toggle {
    background: transparent;
    border: 1px solid #1e2230;
    border-radius: 6px;
    padding: 7px 18px;
    color: #3d3520;
    font-family: 'Cinzel', serif;
    font-size: .65rem;
    letter-spacing: .1em;
    text-transform: uppercase;
    cursor: pointer;
    transition: border-color .2s, color .2s;
  }

  .legend-toggle:hover {
    border-color: #c9a84c44;
    color: #c9a84c;
  }

  .legend {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 10px;
    width: 100%;
    animation: fade-in .2s ease;
  }

  .legend-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 10px 14px;
    background: #0d1117;
    border: 1px solid #1e2230;
    border-radius: 8px;
  }

  .legend-swatch {
    width: 22px;
    height: 22px;
    border-radius: 5px;
    flex-shrink: 0;
    margin-top: 2px;
  }

  .swatch--correct    { background: #1a6b3c; border: 1px solid #2ea555; }
  .swatch--partial    { background: #7a5c00; border: 1px solid #c9a84c; }
  .swatch--incorrect  { background: #4a1515; border: 1px solid #6b1a1a; }
  .swatch--directional{ background: #1a3a6b; border: 1px solid #2563eb; }

  .legend-item strong {
    display: block;
    font-family: 'Cinzel', serif;
    font-size: .7rem;
    color: #c9a84c;
    margin-bottom: 2px;
  }

  .legend-item span {
    font-family: 'Crimson Pro', serif;
    font-size: .85rem;
    color: #5a6470;
    line-height: 1.3;
  }

  /* ── Utilidades ── */
  @keyframes fade-in {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  /* ── Responsive ── */
  @media (max-width: 700px) {
    .col-header-row,
    .empty-slot {
      grid-template-columns: 28px repeat(3, 1fr);
    }

    .col-head:nth-child(n+5) { display: none; }

    .main { padding: 1.5rem 1rem 3rem; gap: 1.5rem; }

    .header { gap: .75rem; }
    .header-rune { display: none; }
  }
</style>