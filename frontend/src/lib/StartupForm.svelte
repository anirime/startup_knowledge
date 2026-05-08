<script>
  let { initial = null, onSave, onCancel } = $props();

  const blank = {
    company_name: '',
    industry: '',
    founded_year: null,
    location: '',
    investment_stage: '',
    total_funding: null,
    vcs: [],
    ceo: '',
    employee_count: null,
    key_members: [],
    description: '',
    website: '',
    tags: []
  };

  const seed = initial ? { ...blank, ...initial } : { ...blank };
  let form = $state(seed);
  let vcsText = $state((seed.vcs || []).join(', '));
  let membersText = $state((seed.key_members || []).join(', '));
  let tagsText = $state((seed.tags || []).join(', '));
  let saving = $state(false);
  let error = $state('');

  const STAGES = ['Pre-Seed', 'Seed', 'Series A', 'Series B', 'Series C', 'Series D', 'Series E', 'Series F+', 'IPO', '인수합병'];

  function splitList(s) {
    return s.split(',').map((x) => x.trim()).filter(Boolean);
  }

  async function submit(e) {
    e.preventDefault();
    if (!form.company_name.trim()) {
      error = '회사명은 필수입니다.';
      return;
    }
    saving = true;
    error = '';
    try {
      const payload = {
        ...form,
        vcs: splitList(vcsText),
        key_members: splitList(membersText),
        tags: splitList(tagsText),
        founded_year: form.founded_year ? Number(form.founded_year) : null,
        total_funding: form.total_funding === '' || form.total_funding == null ? null : Number(form.total_funding),
        employee_count: form.employee_count === '' || form.employee_count == null ? null : Number(form.employee_count)
      };
      await onSave(payload);
    } catch (err) {
      error = err.message;
    } finally {
      saving = false;
    }
  }
</script>

<form onsubmit={submit} class="form">
  <h2>{initial ? '스타트업 정보 수정' : '스타트업 정보 입력'}</h2>

  {#if error}
    <div class="error">{error}</div>
  {/if}

  <section>
    <h3>기본 정보</h3>
    <div class="grid">
      <div class="full">
        <label for="company_name">회사명 *</label>
        <input id="company_name" bind:value={form.company_name} required />
      </div>
      <div>
        <label for="industry">업종</label>
        <input id="industry" bind:value={form.industry} placeholder="핀테크, AI, 헬스케어 등" />
      </div>
      <div>
        <label for="founded_year">설립연도</label>
        <input id="founded_year" type="number" bind:value={form.founded_year} placeholder="2020" />
      </div>
      <div>
        <label for="location">위치</label>
        <input id="location" bind:value={form.location} placeholder="서울, 강남구" />
      </div>
      <div>
        <label for="website">웹사이트</label>
        <input id="website" type="url" bind:value={form.website} placeholder="https://..." />
      </div>
    </div>
  </section>

  <section>
    <h3>투자 정보</h3>
    <div class="grid">
      <div>
        <label for="investment_stage">투자 단계</label>
        <select id="investment_stage" bind:value={form.investment_stage}>
          <option value="">선택...</option>
          {#each STAGES as s}
            <option value={s}>{s}</option>
          {/each}
        </select>
      </div>
      <div>
        <label for="total_funding">누적 투자금 (억원)</label>
        <input id="total_funding" type="number" step="0.1" bind:value={form.total_funding} placeholder="100" />
      </div>
      <div class="full">
        <label for="vcs">주요 VC (쉼표로 구분)</label>
        <input id="vcs" bind:value={vcsText} placeholder="알토스벤처스, 소프트뱅크벤처스" />
      </div>
    </div>
  </section>

  <section>
    <h3>팀 정보</h3>
    <div class="grid">
      <div>
        <label for="ceo">CEO</label>
        <input id="ceo" bind:value={form.ceo} />
      </div>
      <div>
        <label for="employee_count">직원수</label>
        <input id="employee_count" type="number" bind:value={form.employee_count} />
      </div>
      <div class="full">
        <label for="key_members">주요 인력 (쉼표로 구분)</label>
        <input id="key_members" bind:value={membersText} placeholder="CTO 홍길동, COO 김철수" />
      </div>
    </div>
  </section>

  <section>
    <h3>사업 정보</h3>
    <div class="grid">
      <div class="full">
        <label for="description">제품/서비스 설명</label>
        <textarea id="description" rows="4" bind:value={form.description}></textarea>
      </div>
      <div class="full">
        <label for="tags">태그 (쉼표로 구분)</label>
        <input id="tags" bind:value={tagsText} placeholder="B2B, SaaS, AI" />
      </div>
    </div>
  </section>

  <div class="actions">
    <button type="button" onclick={onCancel}>취소</button>
    <button type="submit" class="primary" disabled={saving}>
      {saving ? '저장중...' : '저장'}
    </button>
  </div>
</form>

<style>
  .form { background: white; padding: 24px; border-radius: 12px; border: 1px solid var(--border); }
  h2 { margin-top: 0; }
  h3 { font-size: 14px; color: var(--muted); margin: 24px 0 12px; text-transform: uppercase; letter-spacing: 0.05em; }
  section + section { border-top: 1px solid var(--border); padding-top: 8px; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px 16px; }
  .full { grid-column: 1 / -1; }
  .actions { display: flex; justify-content: flex-end; gap: 8px; margin-top: 24px; }
  .error { background: #fef2f2; color: var(--danger); padding: 10px 12px; border-radius: 8px; margin-bottom: 16px; font-size: 14px; }
  textarea { font-family: inherit; resize: vertical; }
  @media (max-width: 600px) {
    .grid { grid-template-columns: 1fr; }
  }
</style>
