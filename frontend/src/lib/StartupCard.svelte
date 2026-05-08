<script>
  let { startup, onView } = $props();
</script>

<button class="card" onclick={() => onView(startup.id)}>
  <div class="header">
    <h3>{startup.company_name}</h3>
    {#if startup.investment_stage}
      <span class="stage">{startup.investment_stage}</span>
    {/if}
  </div>
  <div class="meta">
    {#if startup.industry}<span>{startup.industry}</span>{/if}
    {#if startup.location}<span>· {startup.location}</span>{/if}
    {#if startup.founded_year}<span>· {startup.founded_year}년</span>{/if}
  </div>
  {#if startup.description}
    <p class="desc">{startup.description}</p>
  {/if}
  {#if startup.tags?.length}
    <div class="tags">
      {#each startup.tags as t}<span class="tag">#{t}</span>{/each}
    </div>
  {/if}
</button>

<style>
  .card {
    width: 100%;
    text-align: left;
    background: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    transition: border-color 0.15s, transform 0.05s, box-shadow 0.15s;
  }
  .card:hover {
    border-color: var(--primary);
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.08);
  }
  .card:active { transform: translateY(1px); }
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
  }
  h3 { margin: 0; font-size: 16px; }
  .stage {
    background: #ecfeff;
    color: #0e7490;
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 999px;
    white-space: nowrap;
  }
  .meta {
    color: var(--muted);
    font-size: 13px;
    margin-top: 4px;
  }
  .meta span { margin-right: 4px; }
  .desc {
    margin: 8px 0 0;
    font-size: 14px;
    color: #374151;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  .tags { margin-top: 8px; }
</style>
