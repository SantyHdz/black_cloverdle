<script lang="ts">
  import { createEventDispatcher, onMount } from 'svelte';
  import { fade, slide } from 'svelte/transition';
  import './GuessInput.css';

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
    <div class="dropdown" bind:this={dropdownEl} role="listbox" in:slide={{ duration: 200, axis: 'y' }}>
      {#each suggestions as name, i (name)}
        <button
          class="suggestion"
          class:suggestion--active={i === activeIndex}
          role="option"
          aria-selected={i === activeIndex}
          onmousedown={(e) => { e.preventDefault(); selectSuggestion(name); }}
          onmouseenter={() => (activeIndex = i)}
          in:fade={{ duration: 100, delay: i * 30 }}
        >
          <span class="suggestion-rune">✦</span>
          <span class="suggestion-name">{name}</span>
        </button>
      {/each}
    </div>
  {/if}
</div>