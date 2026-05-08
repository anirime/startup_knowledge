<script>
  let { startup, onEdit, onDelete, onClose } = $props();

  function formatFunding(v) {
    if (v == null) return '-';
    return `${v.toLocaleString()} 억원`;
  }
</script>

<div class="detail">
  <div class="top">
    <button onclick={onClose}>← 목록으로</button>
    <div class="actions">
      <button onclick={() => onEdit(startup)}>수정</button>
      <button class="danger" onclick={() => onDelete(startup)}>삭제</button>
    </div>
  </div>

  <header>
    <h1>{startup.company_name}</h1>
    <div class="meta">
      {#if startup.industry}<span>{startup.industry}</span>{/if}
      {#if startup.location}<span>· {startup.location}</span>{/if}
      {#if startup.founded_year}<span>· {startup.founded_year}년 설립</span>{/if}
      {#if startup.website}
        <span>·
          <a href={startup.website} target="_blank" rel="noopener">웹사이트 ↗</a>
        </span>
      {/if}
    </div>
    {#if startup.tags?.length}
      <div class="tags">
        {#each startup.tags as t}<span class="tag">#{t}</span>{/each}
      </div>
    {/if}
  </header>

  {#if startup.description}
    <section>
      <h3>제품/서비스</h3>
      <p>{startup.description}</p>
    </section>
  {/if}

  <section>
    <h3>투자 정보</h3>
    <dl>
      <dt>투자 단계</dt><dd>{startup.investment_stage || '-'}</dd>
      <dt>누적 투자금</dt><dd>{formatFunding(startup.total_funding)}</dd>
      <dt>주요 VC</dt><dd>{startup.vcs?.length ? startup.vcs.join(', ') : '-'}</dd>
    </dl>
  </section>

  <section>
    <h3>팀</h3>
    <dl>
      <dt>CEO</dt><dd>{startup.ceo || '-'}</dd>
      <dt>직원수</dt><dd>{startup.employee_count != null ? `${startup.employee_count}명` : '-'}</dd>
      <dt>주요 인력</dt><dd>{startup.key_members?.length ? startup.key_members.join(', ') : '-'}</dd>
    </dl>
  </section>
</div>

<style>
  .detail { background: white; border: 1px solid var(--border); border-radius: 12px; padding: 24px; }
  .top { display: flex; justify-content: space-between; margin-bottom: 16px; }
  .actions { display: flex; gap: 8px; }
  header { border-bottom: 1px solid var(--border); padding-bottom: 16px; margin-bottom: 16px; }
  h1 { margin: 0 0 8px; }
  .meta { color: var(--muted); font-size: 14px; }
  .meta span { margin-right: 4px; }
  .meta a { color: var(--primary); text-decoration: none; }
  .meta a:hover { text-decoration: underline; }
  .tags { margin-top: 8px; }
  section { margin-top: 20px; }
  h3 { font-size: 13px; color: var(--muted); margin: 0 0 8px; text-transform: uppercase; letter-spacing: 0.05em; }
  p { margin: 0; line-height: 1.6; white-space: pre-wrap; }
  dl { display: grid; grid-template-columns: 140px 1fr; gap: 8px 16px; margin: 0; }
  dt { color: var(--muted); font-size: 14px; }
  dd { margin: 0; font-size: 14px; }
</style>
