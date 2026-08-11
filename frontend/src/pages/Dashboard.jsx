import PixelCard from "../components/PixelCard/PixelCard";
import Radar from "../components/Radar/Radar";

function Dashboard() {
  return (
    <main className="dashboard">

      <section className="hero">

        <div className="hero-content">
          <span className="status">
            ● SISTEMA ONLINE
          </span>

          <h1>
            Promo<span>Watch</span>
          </h1>

          <p>
            Monitorando promoções dos seus
            produtos favoritos.
          </p>
        </div>

        <div className="radar">
            <Radar
            speed={0.4}
            scale={0.5}
            ringCount={6}
            spokeCount={6}
            ringThickness={0.04}
            spokeThickness={0.008}
            sweepSpeed={0.7}
            sweepWidth={2}
            color="#38bdf8"
            backgroundColor="#020617"
            brightness={0.9}
            enableMouseInteraction={false}
            />
        </div>

      </section>


      <section className="stats">

        <div className="stat">
          <span>Produtos</span>
          <strong>3</strong>
        </div>

        <div className="stat">
          <span>Grupos</span>
          <strong>4</strong>
        </div>

        <div className="stat">
          <span>Promoções</span>
          <strong>27</strong>
        </div>

        <div className="stat">
          <span>Status</span>
          <strong className="online">
            ONLINE
          </strong>
        </div>

      </section>


      <section className="products">

        <div className="section-header">
          <div>
            <span className="section-label">
              MONITORAMENTO
            </span>

            <h2>
              Seus desejos
            </h2>
          </div>

          <button>
            + Adicionar produto
          </button>
        </div>


        <div className="product-grid">

          <PixelCard variant="blue">

            <div className="product-card">

              <div className="product-icon">
                🖥️
              </div>

              <h3>
                LG Ultragear 32GN600
              </h3>

              <p>
                Monitor 32" QHD 165Hz
              </p>

              <div className="price">
                <span>Preço máximo</span>

                <strong>
                  R$ 1.000,00
                </strong>
              </div>

              <div className="product-status">
                <span>●</span>
                Monitorando
              </div>

            </div>

          </PixelCard>


          <PixelCard variant="yellow">

            <div className="product-card">

              <div className="product-icon">
                🎮
              </div>

              <h3>
                PlayStation 5
              </h3>

              <p>
                Console PlayStation 5
              </p>

              <div className="price">
                <span>Preço máximo</span>

                <strong>
                  R$ 3.500,00
                </strong>
              </div>

              <div className="product-status">
                <span>●</span>
                Monitorando
              </div>

            </div>

          </PixelCard>


          <PixelCard variant="pink">

            <div className="product-card">

              <div className="product-icon">
                📱
              </div>

              <h3>
                iPhone 15
              </h3>

              <p>
                Apple iPhone 15
              </p>

              <div className="price">
                <span>Preço máximo</span>

                <strong>
                  R$ 3.000,00
                </strong>
              </div>

              <div className="product-status">
                <span>●</span>
                Monitorando
              </div>

            </div>

          </PixelCard>

        </div>

      </section>

    </main>
  );
}

export default Dashboard;