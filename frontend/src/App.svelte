<script>
  import { onMount } from 'svelte';
  import StartupCard from './lib/StartupCard.svelte';
  import StartupForm from './lib/StartupForm.svelte';
  import StartupDetail from './lib/StartupDetail.svelte';
  import {
    listStartups,
    createStartup,
    updateStartup,
    deleteStartup,
    getStartup,
    getFacets
  } from './api.js';

  let view = $state('list'); // 'list' | 'form' | 'detail'
  let editing = $state(null);
  let detail = $state(null);

  let startups = $state([]);
  let facets = $state({ industries: [], stages: [], locations: [], tags: [] });
  let loading = $state(false);
  let errorMsg = $state('');

  let q = $state('');
  let nameFilter = $state('');
  let industryFilter = $state('');
  let stageFilter = $state('');
  let locationFilter = $state('');
  let tagFilter = $state('');

  let searchTimer;

  async function refresh() {
    loading = true;
    errorMsg = '';
    try {
      const params = {
        q: q.trim(),
        name: nameFilter.trim(),
        industry: industryFilter,
        stage: stageFilter,
        location: locationFilter,
        tag: tagFilter
      };
      [startups, facets] = await Promise.all([listStartups(params), getFacets()]);
    } catch (e) {
      errorMsg = e.message;
    } finally {
      loading = false;
    }
  }

  function debouncedRefresh() {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(refresh, 250);
  }

  function clearFilters() {
    q = '';
    nameFilter = '';
    industryFilter = '';
    stageFilter = '';
    locationFilter = '';
    tagFilter = '';
    refresh();
  }

  async function openDetail(id) {
    try {
      detail = await getStartup(id);
      view = 'detail';
    } catch (e) {
      errorMsg = e.message;
    }
  }

  function openNew() {
    editing = null;
    view = 'form';
  }

  function openEdit(s) {
    editing = s;
    view = 'form';
  }

  async function handleSave(payload) {
    if (editing) {
      const updated = await updateStartup(editing.id, payload);
      detail = updated;
      view = 'detail';
    } else {
      const created = await createStartup(payload);
      detail = created;
      view = 'detail';
    }
    refresh();
  }

  async function handleDelete(s) {
    if (!confirm(`${s.company_name}을(를) 삭제하시겠습니까?`)) return;
    try {
      await deleteStartup(s.id);
      view = 'list';
      detail = null;
      refresh();
    } catch (e) {
      errorMsg = e.message;
    }
  }

  onMount(refresh);
</script>

<div class="page">
  <header class="topbar">
    <h1>🚀 스타트업 지식베이스</h1>
    {#if view === 'list'}
      <button class="primary" onclick={openNew}>+ 새 스타트업 등록</button>
    {/if}
  </header>

  {#if errorMsg}
    <div class="error">{errorMsg}</div>
  {/if}

  {#if view === 'list'}
    <div class="search">
      <input
        type="search"
        placeholder="🔍 전체 검색 (회사명, 설명, 인력, VC, 태그 등)"
        bind:value={q}
        oninput={debouncedRefresh}
      />
      <div class="filters">
        <input placeholder="회사명" bind:value={nameFilter} oninput={debouncedRefresh} />
        <select bind:value={industryFilter} onchange={refresh}>
          <option value="">전체 업종</option>
          {#each facets.industries as v}<option value={v}>{v}</option>{/each}
        </select>
        <select bind:value={stageFilter} onchange={refresh}>
          <option value="">전체 단계</option>
          {#each facets.stages as v}<option value={v}>{v}</option>{/each}
        </select>
        <select bind:value={locationFilter} onchange={refresh}>
          <option value="">전체 지역</option>
          {#each facets.locations as v}<option value={v}>{v}</option>{/each}
        </select>
        <select bind:value={tagFilter} onchange={refresh}>
          <option value="">전체 태그</option>
          {#each facets.tags as v}<option value={v}>#{v}</option>{/each}
        </select>
        <button onclick={clearFilters}>초기화</button>
      </div>
    </div>

    <div class="results-meta">
      {loading ? '불러오는 중...' : `${startups.length}개 결과`}
    </div>

    {#if !loading && startups.length === 0}
      <div class="empty">
        등록된 스타트업이 없습니다. 우측 상단의 <strong>+ 새 스타트업 등록</strong> 버튼으로 시작하세요.
      </div>
    {:else}
      <div class="grid">
        {#each startups as s (s.id)}
          <StartupCard startup={s} onView={openDetail} />
        {/each}
      </div>
    {/if}
  {:else if view === 'form'}
    <StartupForm
      initial={editing}
      onSave={handleSave}
      onCancel={() => (view = editing ? 'detail' : 'list')}
    />
  {:else if view === 'detail' && detail}
    <StartupDetail
      startup={detail}
      onEdit={openEdit}
      onDelete={handleDelete}
      onClose={() => (view = 'list')}
    />
  {/if}
</div>

<style>
  .page { max-width: 1100px; margin: 0 auto; padding: 24px; }
  .topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
  }
  h1 { margin: 0; font-size: 22px; }
  .search {
    background: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
  }
  .filters {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)) auto;
    gap: 8px;
    margin-top: 12px;
  }
  .results-meta {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 12px;
  }
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 12px;
  }
  .empty {
    background: white;
    border: 1px dashed var(--border);
    border-radius: 12px;
    padding: 48px 16px;
    text-align: center;
    color: var(--muted);
  }
  .error {
    background: #fef2f2;
    color: var(--danger);
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 16px;
  }
</style>
