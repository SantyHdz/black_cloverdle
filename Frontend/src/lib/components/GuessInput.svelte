<script lang="ts">
  import { createEventDispatcher, onMount } from 'svelte';

  //Props en svelte usando runes
  let {
    disabled = false,
    placeholder = 'Escribe el nombre de un personaje...'
  } = $props<{
    disabled?: boolean;
    placeholder?: string;
  }>();

  const dispatch = createEventDispatcher<{ guess: string }>();

  // Estado reactivo con $state() para Svelte 5
  let query = $state('');
  let suggestions = $state<string[]>([]);
  let loading = $state(false);
  let open = $state(false);
  let activeIndex = $state(-1);
  let inputEl: HTMLInputElement;
  let dropdownEl: HTMLDivElement;

  let debounceTimer: ReturnType<typeof setTimeout>;

  async function fetchSuggestions(q: string) {
    if (q.trim().length < 1) {
      suggestions = [];
      open = false;
      return;
    }
    loading = true;
    try {
      const res = await fetch(`/api/characters/search?q=${encodeURIComponent(q)}&limit=8`);
      const data = await res.json();
      suggestions = data.results ?? [];
      open = suggestions.length > 0;
      activeIndex = -1;
    } catch {
      suggestions = [];
      open = false;
    } finally {
      loading = false;
    }
  }

  function onInput() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => fetchSuggestions(query), 200);
  }

  function selectSuggestion(name: string) {
    query = name;
    open = false;
    activeIndex = -1;
    inputEl?.focus();
  }

  function submitGuess() {
    const trimmed = query.trim();
    if (!trimmed || disabled) return;
    dispatch('guess', trimmed);
    query = '';
    suggestions = [];
    open = false;
  }

  function onKeyDown(e: KeyboardEvent) {
    if (!open) {
      if (e.key === 'Enter') submitGuess();
      return;
    }
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      activeIndex = Math.min(activeIndex + 1, suggestions.length - 1);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      activeIndex = Math.max(activeIndex - 1, -1);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (activeIndex >= 0) {
        selectSuggestion(suggestions[activeIndex]);
      } else {
        submitGuess();
      }
    } else if (e.key === 'Escape') {
      open = false;
      activeIndex = -1;
    }
  }

  function onClickOutside(e: MouseEvent) {
    if (!inputEl?.contains(e.target as Node) && !dropdownEl?.contains(e.target as Node)) {
      open = false;
    }
  }

  onMount(() => {
  const handler = (e: MouseEvent) => onClickOutside(e);

  document.addEventListener('mousedown', handler);

  return () => {
    document.removeEventListener('mousedown', handler);
  };
});
</script>

<div class="guess-input-root">
  <div class="input-row">
    <!-- Campo de texto -->
    <div class="input-wrapper" class:input-wrapper--open={open}>
      <span class="input-icon">
        {#if loading}
          <span class="spinner"></span>
        {:else}
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <path d="m21 21-4.35-4.35"/>
          </svg>
        {/if}
      </span>

      <input
        bind:this={inputEl}
        bind:value={query}
        oninput={onInput}
        onkeydown={onKeyDown}
        type="text"
        {placeholder}
        {disabled}
        autocomplete="off"
        spellcheck="false"
        aria-autocomplete="list"
      />
    </div>

    <!-- Botón de enviar -->
    <button
      class="submit-btn"
      onclick={submitGuess}
      {disabled}
      aria-label="Adivinar personaje"
    >
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <path d="M5 12h14M12 5l7 7-7 7"/>
      </svg>
      <span>Adivinar</span>
    </button>
  </div>

  <!-- Dropdown de sugerencias -->
  {#if open && suggestions.length > 0}
    <div class="dropdown" bind:this={dropdownEl} role="listbox">
      {#each suggestions as name, i}
        <button
          class="suggestion"
          class:suggestion--active={i === activeIndex}
          role="option"
          aria-selected={i === activeIndex}
          onmousedown={(e) => { e.preventDefault(); selectSuggestion(name); }}
          onmouseenter={() => (activeIndex = i)}
        >
          <span class="suggestion-rune">✦</span>
          <span class="suggestion-name">{name}</span>
        </button>
      {/each}
    </div>
  {/if}
</div>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Pro:wght@400;600&display=swap');

  .guess-input-root {
    position: relative;
    width: 100%;
    max-width: 640px;
    font-family: 'Crimson Pro', serif;
  }

  .input-row {
    display: flex;
    gap: 10px;
    align-items: stretch;
  }

  /* ── Campo de texto ── */
  .input-wrapper {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0 14px;
    background: #0d1117;
    border: 1px solid #3a3010;
    border-radius: 10px;
    transition: border-color 0.2s, box-shadow 0.2s;
    min-width: 0;
  }

  .input-wrapper:focus-within,
  .input-wrapper--open {
    border-color: #c9a84c;
    box-shadow: 0 0 0 3px rgba(201, 168, 76, 0.12);
  }

  .input-icon {
    color: #5a4d2a;
    display: flex;
    align-items: center;
    flex-shrink: 0;
  }

  .input-wrapper:focus-within .input-icon {
    color: #c9a84c;
  }

  input {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: #e6edf3;
    font-family: 'Crimson Pro', serif;
    font-size: 1rem;
    padding: 14px 0;
    min-width: 0;
  }

  input::placeholder {
    color: #3d3520;
  }

  input:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  /* ── Spinner ── */
  .spinner {
    width: 14px;
    height: 14px;
    border: 2px solid #3a3010;
    border-top-color: #c9a84c;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    display: block;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  /* ── Botón enviar ── */
  .submit-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0 20px;
    background: linear-gradient(135deg, #2a1f05 0%, #4a3510 50%, #2a1f05 100%);
    border: 1px solid #c9a84c;
    border-radius: 10px;
    color: #c9a84c;
    font-family: 'Cinzel', serif;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    cursor: pointer;
    transition: background 0.2s, box-shadow 0.2s, transform 0.1s;
    white-space: nowrap;
  }

  .submit-btn:hover:not(:disabled) {
    background: linear-gradient(135deg, #3a2a08 0%, #6a4e18 50%, #3a2a08 100%);
    box-shadow: 0 0 14px rgba(201, 168, 76, 0.3);
  }

  .submit-btn:active:not(:disabled) {
    transform: scale(0.97);
  }

  .submit-btn:disabled {
    opacity: 0.35;
    cursor: not-allowed;
  }

  /* ── Dropdown ── */
  .dropdown {
    position: absolute;
    top: calc(100% + 6px);
    left: 0;
    right: 0;
    background: #0f1318;
    border: 1px solid #c9a84c66;
    border-radius: 10px;
    overflow: hidden;
    z-index: 100;
    animation: dropdown-in 0.15s ease;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
  }

  @keyframes dropdown-in {
    from { opacity: 0; transform: translateY(-6px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .suggestion {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 16px;
    background: transparent;
    border: none;
    border-bottom: 1px solid #1c2030;
    color: #a89060;
    font-family: 'Crimson Pro', serif;
    font-size: 0.95rem;
    cursor: pointer;
    text-align: left;
    transition: background 0.12s, color 0.12s;
  }

  .suggestion:last-child {
    border-bottom: none;
  }

  .suggestion--active,
  .suggestion:hover {
    background: #1a1505;
    color: #e6c87a;
  }

  .suggestion-rune {
    font-size: 0.6rem;
    color: #5a4020;
    flex-shrink: 0;
    transition: color 0.12s;
  }

  .suggestion--active .suggestion-rune,
  .suggestion:hover .suggestion-rune {
    color: #c9a84c;
  }

  .suggestion-name {
    font-weight: 600;
  }
</style>