import { useCallback, useEffect, useState } from "react";
import Radar from "./components/Radar/Radar";
import PixelCard from "./components/PixelCard/PixelCard";
import "./App.css";

const EMPTY_FORM = {
  id: null,
  name: "",
  description: "",
  keywords: [],
  max_price: "",
  icon: "📦",
};

const EMPTY_GROUP_FORM = { name: "", id: "" };

const currency = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

function App() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState(EMPTY_FORM);
  const [keywordInput, setKeywordInput] = useState("");
  const [showGroupForm, setShowGroupForm] = useState(false);
  const [groupForm, setGroupForm] = useState(EMPTY_GROUP_FORM);
  const [showTelegramGroups, setShowTelegramGroups] = useState(false);
  const [telegramGroups, setTelegramGroups] = useState([]);
  const [loadingTelegramGroups, setLoadingTelegramGroups] = useState(false);
  const [telegramGroupsUpdatedAt, setTelegramGroupsUpdatedAt] = useState(null);

  const loadDashboard = useCallback(async () => {
    try {
      const response = await fetch("/api/dashboard");
      if (!response.ok) throw new Error("Backend indisponível");
      const data = await response.json();
      setDashboard({
        ...data,
        products: Array.isArray(data.products) ? data.products : [],
        groups: Array.isArray(data.groups) ? data.groups : [],
        recent_promotions: Array.isArray(data.recent_promotions) ? data.recent_promotions : [],
      });
      setError("");
    } catch (requestError) {
      setError(`${requestError.message}. Inicie a API Python na porta 8000.`);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);

  const handleChange = (event) => {
    setForm((current) => ({ ...current, [event.target.name]: event.target.value }));
  };

  const handleAddKeyword = () => {
    const trimmed = keywordInput.trim();
    if (!trimmed) return;
    if (!form.keywords.includes(trimmed)) {
      setForm((current) => ({
        ...current,
        keywords: [...current.keywords, trimmed],
      }));
    }
    setKeywordInput("");
  };

  const handleRemoveKeyword = (keywordToRemove) => {
    setForm((current) => ({
      ...current,
      keywords: current.keywords.filter((k) => k !== keywordToRemove),
    }));
  };

  const handleKeywordKeyDown = (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      handleAddKeyword();
    }
  };

  const startEditingProduct = (product) => {
    setForm({
      id: product.id,
      name: product.name,
      description: product.description || "",
      keywords: Array.isArray(product.keywords) ? [...product.keywords] : [product.name],
      max_price: product.max_price,
      icon: product.icon || "📦",
    });
    setKeywordInput("");
    setShowForm(true);
    setTimeout(() => {
      const formEl = document.querySelector(".product-form");
      if (formEl) {
        formEl.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }, 50);
  };

  const handleCancelForm = () => {
    setForm(EMPTY_FORM);
    setKeywordInput("");
    setShowForm(false);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!form.name.trim()) {
      setError("Informe o nome do produto.");
      return;
    }
    if (!form.keywords || form.keywords.length === 0) {
      setError("Adicione pelo menos uma palavra-chave para o monitoramento.");
      return;
    }
    setSaving(true);
    setError("");
    try {
      const isEditing = Boolean(form.id);
      const url = isEditing ? `/api/products/${form.id}` : "/api/products";
      const method = isEditing ? "PUT" : "POST";

      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || "Não foi possível salvar");
      setForm(EMPTY_FORM);
      setKeywordInput("");
      setShowForm(false);
      await loadDashboard();
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setSaving(false);
    }
  };

  const removeProduct = async (product) => {
    if (!window.confirm(`Remover ${product.name} do monitoramento?`)) return;
    try {
      const response = await fetch(`/api/products/${product.id}`, { method: "DELETE" });
      if (!response.ok) throw new Error("Não foi possível remover o produto");
      if (form.id === product.id) {
        handleCancelForm();
      }
      await loadDashboard();
    } catch (requestError) {
      setError(requestError.message);
    }
  };

  const handleGroupSubmit = async (event) => {
    event.preventDefault();
    setSaving(true);
    setError("");
    try {
      const response = await fetch("/api/groups", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(groupForm),
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || "Não foi possível salvar o grupo");
      setGroupForm(EMPTY_GROUP_FORM);
      setShowGroupForm(false);
      await loadDashboard();
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setSaving(false);
    }
  };

  const removeGroup = async (group) => {
    if (!window.confirm(`Remover ${group.name} do monitoramento?`)) return;
    try {
      const response = await fetch(`/api/groups/${group.id}`, { method: "DELETE" });
      if (!response.ok) throw new Error("Não foi possível remover o grupo");
      await loadDashboard();
    } catch (requestError) {
      setError(requestError.message);
    }
  };

  const findTelegramGroups = async () => {
    setLoadingTelegramGroups(true);
    setError("");
    try {
      const response = await fetch("/api/telegram/groups");
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || "Não foi possível buscar os grupos");
      setTelegramGroups(Array.isArray(result.groups) ? result.groups : []);
      setTelegramGroupsUpdatedAt(result.updated_at ?? null);
      setShowTelegramGroups(true);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoadingTelegramGroups(false);
    }
  };

  const addTelegramGroup = async (group) => {
    setSaving(true);
    setError("");
    try {
      const response = await fetch("/api/groups", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: group.id, name: group.name }),
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || "Não foi possível adicionar o grupo");
      await loadDashboard();
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setSaving(false);
    }
  };

  const stats = dashboard?.stats ?? { products: 0, groups: 0, promotions: 0, status: "offline" };
  const apiStatus = typeof stats.status === "string" ? stats.status.toUpperCase() : "ONLINE";

  return (
    <div className="app">
      <Radar
        speed={0.4}
        scale={0.5}
        ringCount={8}
        spokeCount={12}
        ringThickness={0.04}
        spokeThickness={0.008}
        sweepSpeed={0.8}
        sweepWidth={3}
        sweepLobes={1}
        color="#9f29ff"
        backgroundColor="#050509"
        falloff={2}
        brightness={0.7}
        enableMouseInteraction
        mouseInfluence={0.08}
      />

      <main className="app-content">
        <section className="dashboard">
          <section className="hero">
            <div className="hero-content">
              <span className={`status ${error ? "offline" : ""}`}>
                ● SISTEMA {error ? "OFFLINE" : "ONLINE"}
              </span>
              <h1>Telegram<br /><span>Promoções</span></h1>
              <p>Monitoramento inteligente de promoções nos grupos do Telegram.</p>
            </div>
          </section>

          {error && <div className="error-banner" role="alert">{error}</div>}

          <section className="stats">
            <div className="stat"><span>PRODUTOS MONITORADOS</span><strong>{stats.products}</strong></div>
            <div className="stat"><span>GRUPOS MONITORADOS</span><strong>{stats.groups}</strong></div>
            <div className="stat"><span>PROMOÇÕES ENCONTRADAS</span><strong>{stats.promotions}</strong></div>
            <div className="stat"><span>STATUS DA API</span><strong className={error ? "offline" : "online"}>{error ? "OFFLINE" : apiStatus}</strong></div>
          </section>

          <section className="groups-section">
            <div className="section-header">
              <div><span className="section-label">FONTES</span><h2>Grupos do Telegram</h2></div>
              <div className="section-actions">
                <button className="secondary-button" type="button" onClick={findTelegramGroups} disabled={loadingTelegramGroups}>
                  {loadingTelegramGroups ? "Buscando..." : "Buscar no Telegram"}
                </button>
                <button type="button" onClick={() => setShowGroupForm((visible) => !visible)}>
                  {showGroupForm ? "Cancelar" : "+ Informar ID"}
                </button>
              </div>
            </div>

            {showTelegramGroups && (
              <div className="telegram-picker">
                <div className="picker-header">
                  <div>
                    <strong>Grupos e canais disponíveis</strong>
                    <span>
                      {telegramGroupsUpdatedAt
                        ? `Sincronizado em ${new Date(telegramGroupsUpdatedAt).toLocaleString("pt-BR")}`
                        : "Inicie o monitor para sincronizar a sua conta do Telegram."}
                    </span>
                  </div>
                  <button type="button" onClick={() => setShowTelegramGroups(false)} aria-label="Fechar lista">×</button>
                </div>
                <div className="telegram-picker-list">
                  {telegramGroups.map((group) => {
                    const alreadyAdded = (dashboard?.groups ?? []).some((saved) => String(saved.id) === String(group.id));
                    return (
                      <article className="telegram-picker-item" key={group.id}>
                        <div><strong>{group.name}</strong><span>{group.type === "channel" ? "Canal" : "Grupo"} · {group.id}</span></div>
                        <button type="button" disabled={alreadyAdded || saving} onClick={() => addTelegramGroup(group)}>
                          {alreadyAdded ? "Adicionado" : "Adicionar"}
                        </button>
                      </article>
                    );
                  })}
                  {!telegramGroups.length && <p className="empty-message">Nenhum grupo sincronizado ainda.</p>}
                </div>
              </div>
            )}

            {showGroupForm && (
              <form className="group-form" onSubmit={handleGroupSubmit}>
                <label>Nome do grupo<input value={groupForm.name} onChange={(event) => setGroupForm((current) => ({ ...current, name: event.target.value }))} placeholder="Ex.: Promoções de hardware" required /></label>
                <label>ID do grupo<input value={groupForm.id} onChange={(event) => setGroupForm((current) => ({ ...current, id: event.target.value }))} placeholder="Ex.: -1001234567890" inputMode="numeric" pattern="-?[0-9]+" required /></label>
                <button type="submit" disabled={saving}>{saving ? "Salvando..." : "Salvar grupo"}</button>
              </form>
            )}

            <div className="group-list">
              {(dashboard?.groups ?? []).map((group) => (
                <article className="group-item" key={group.id}>
                  <div className="group-icon">✈</div>
                  <div><strong>{group.name}</strong><span>{group.id}</span></div>
                  <span className="group-active">● ATIVO</span>
                  <button type="button" onClick={() => removeGroup(group)} aria-label={`Remover ${group.name}`}>×</button>
                </article>
              ))}
              {!loading && !dashboard?.groups.length && <p className="empty-message">Nenhum grupo monitorado.</p>}
            </div>
          </section>

          <section>
            <div className="section-header">
              <div><span className="section-label">MONITORAMENTO</span><h2>Seus produtos</h2></div>
              <button
                type="button"
                onClick={() => {
                  if (showForm) {
                    handleCancelForm();
                  } else {
                    setForm(EMPTY_FORM);
                    setKeywordInput("");
                    setShowForm(true);
                  }
                }}
              >
                {showForm ? "Cancelar" : "+ Adicionar produto"}
              </button>
            </div>

            {showForm && (
              <form className="product-form" onSubmit={handleSubmit}>
                <div className="form-header-badge">
                  <span>{form.id ? "✏️ EDITANDO PRODUTO" : "✨ NOVO PRODUTO"}</span>
                </div>

                <label>
                  Nome
                  <input
                    name="name"
                    value={form.name}
                    onChange={handleChange}
                    placeholder="Ex.: Monitor Gamer 144Hz"
                    required
                  />
                </label>

                <label>
                  Descrição
                  <input
                    name="description"
                    value={form.description}
                    onChange={handleChange}
                    placeholder="Ex.: Monitor IPS 24 polegadas"
                  />
                </label>

                <label>
                  Preço máximo (R$)
                  <input
                    name="max_price"
                    type="number"
                    min="0.01"
                    step="0.01"
                    value={form.max_price}
                    onChange={handleChange}
                    placeholder="Ex.: 899.90"
                    required
                  />
                </label>

                <label>
                  Ícone / Emoji
                  <input
                    name="icon"
                    value={form.icon}
                    onChange={handleChange}
                    maxLength="4"
                    placeholder="📦"
                  />
                </label>

                <div className="keywords-manager">
                  <label>
                    Palavras-chave de busca
                    <span className="keywords-hint">
                      (O robô usará essas palavras para encontrar as promoções no chat)
                    </span>
                  </label>
                  <div className="keywords-input-row">
                    <input
                      type="text"
                      value={keywordInput}
                      onChange={(e) => setKeywordInput(e.target.value)}
                      onKeyDown={handleKeywordKeyDown}
                      placeholder="Digite uma palavra-chave (ex: 32gn600) e clique em Adicionar"
                    />
                    <button
                      type="button"
                      onClick={handleAddKeyword}
                      className="add-keyword-button"
                    >
                      + Adicionar
                    </button>
                  </div>

                  <div className="keyword-tags-container">
                    {form.keywords.map((kw, idx) => (
                      <span key={idx} className="keyword-chip">
                        <span className="chip-text">{kw}</span>
                        <button
                          type="button"
                          onClick={() => handleRemoveKeyword(kw)}
                          className="chip-remove"
                          aria-label={`Remover ${kw}`}
                        >
                          ×
                        </button>
                      </span>
                    ))}
                    {form.keywords.length === 0 && (
                      <span className="no-keywords-message">
                        Nenhuma palavra-chave adicionada ainda. Digite acima e clique em <strong>+ Adicionar</strong> (ou pressione Enter).
                      </span>
                    )}
                  </div>
                </div>

                <div className="form-action-buttons">
                  <button type="button" className="cancel-form-button" onClick={handleCancelForm}>
                    Cancelar
                  </button>
                  <button type="submit" className="submit-form-button" disabled={saving}>
                    {saving ? "Salvando..." : form.id ? "💾 Salvar Alterações" : "Salvar produto"}
                  </button>
                </div>
              </form>
            )}

            {loading ? (
              <p className="loading-message">Carregando produtos...</p>
            ) : (
              <div className="product-grid">
                {(dashboard?.products ?? []).map((product, index) => (
                  <PixelCard
                    key={product.id}
                    variant={["blue", "yellow", "pink"][index % 3]}
                    className="product-card product-pixel-card"
                  >
                    <div className="card-actions">
                      <button
                        className="edit-product"
                        type="button"
                        onClick={() => startEditingProduct(product)}
                        aria-label={`Editar ${product.name}`}
                        title="Editar produto"
                      >
                        ✏️
                      </button>
                      <button
                        className="remove-product"
                        type="button"
                        onClick={() => removeProduct(product)}
                        aria-label={`Remover ${product.name}`}
                        title="Remover produto"
                      >
                        ×
                      </button>
                    </div>

                    <div className="product-icon">{product.icon || "📦"}</div>
                    <h3>{product.name}</h3>
                    <p>{product.description}</p>

                    <div className="product-keywords-preview">
                      {(product.keywords || []).map((kw, i) => (
                        <span key={i} className="card-keyword-tag">
                          {kw}
                        </span>
                      ))}
                    </div>

                    <div className="price">
                      <span>PREÇO MÁXIMO</span>
                      <strong>{currency.format(product.max_price)}</strong>
                    </div>
                    <div className="product-status"><span>●</span> Monitorando</div>
                  </PixelCard>
                ))}
                {!dashboard?.products.length && <p className="empty-message">Nenhum produto monitorado.</p>}
              </div>
            )}
          </section>
        </section>
      </main>
    </div>
  );
}

export default App;
