import { useEffect, useRef } from "react";
import "./PixelCard.css";

class Pixel {
  constructor(canvas, context, x, y, color, speed, delay) {
    this.width = canvas.width;
    this.height = canvas.height;
    this.ctx = context;

    this.x = x;
    this.y = y;

    this.color = color;

    this.speed = this.getRandomValue(0.1, 0.9) * speed;

    this.size = 0;

    this.sizeStep = Math.random() * 0.4;

    this.minSize = 0.5;
    this.maxSizeInteger = 2;

    this.maxSize = this.getRandomValue(
      this.minSize,
      this.maxSizeInteger
    );

    this.delay = delay;

    this.counter = 0;

    this.counterStep =
      Math.random() * 4 +
      (this.width + this.height) * 0.01;

    this.isIdle = false;
    this.isReverse = false;
    this.isShimmer = false;
  }

  getRandomValue(min, max) {
    return Math.random() * (max - min) + min;
  }

  draw() {
    const centerOffset =
      this.maxSizeInteger * 0.5 -
      this.size * 0.5;

    this.ctx.fillStyle = this.color;

    this.ctx.fillRect(
      this.x + centerOffset,
      this.y + centerOffset,
      this.size,
      this.size
    );
  }

  appear() {
    this.isIdle = false;

    if (this.counter <= this.delay) {
      this.counter += this.counterStep;
      return;
    }

    if (this.size >= this.maxSize) {
      this.isShimmer = true;
    }

    if (this.isShimmer) {
      this.shimmer();
    } else {
      this.size += this.sizeStep;
    }

    this.draw();
  }

  disappear() {
    this.isShimmer = false;

    this.counter = 0;

    if (this.size <= 0) {
      this.isIdle = true;
      return;
    }

    this.size -= 0.1;

    this.draw();
  }

  shimmer() {
    if (this.size >= this.maxSize) {
      this.isReverse = true;
    } else if (this.size <= this.minSize) {
      this.isReverse = false;
    }

    if (this.isReverse) {
      this.size -= this.speed;
    } else {
      this.size += this.speed;
    }
  }
}

function getEffectiveSpeed(value, reducedMotion) {
  const min = 0;
  const max = 100;
  const throttle = 0.001;

  const parsed = parseInt(value, 10);

  if (parsed <= min || reducedMotion) {
    return min;
  }

  if (parsed >= max) {
    return max * throttle;
  }

  return parsed * throttle;
}

const VARIANTS = {
  default: {
    gap: 5,
    speed: 35,
    colors: "#f8fafc,#f1f5f9,#cbd5e1",
    noFocus: false,
  },

  blue: {
    gap: 10,
    speed: 25,
    colors: "#e0f2fe,#7dd3fc,#0ea5e9",
    noFocus: false,
  },

  yellow: {
    gap: 3,
    speed: 20,
    colors: "#fef08a,#fde047,#eab308",
    noFocus: false,
  },

  pink: {
    gap: 6,
    speed: 80,
    colors: "#fecdd3,#fda4af,#e11d48",
    noFocus: true,
  },
};

export default function PixelCard({
  variant = "default",
  gap,
  speed,
  colors,
  noFocus,
  className = "",
  children,
}) {
  const containerRef = useRef(null);
  const canvasRef = useRef(null);

  const pixelsRef = useRef([]);

  const animationRef = useRef(null);

  const timePreviousRef = useRef(
    performance.now()
  );

  const reducedMotion = useRef(
    typeof window !== "undefined" &&
      window.matchMedia(
        "(prefers-reduced-motion: reduce)"
      ).matches
  ).current;

  const variantCfg =
    VARIANTS[variant] || VARIANTS.default;

  const finalGap =
    gap ?? variantCfg.gap;

  const finalSpeed =
    speed ?? variantCfg.speed;

  const finalColors =
    colors ?? variantCfg.colors;

  const finalNoFocus =
    noFocus ?? variantCfg.noFocus;

  // =========================================================
  // INICIALIZAR PIXELS
  // =========================================================

  const initPixels = () => {
    if (
      !containerRef.current ||
      !canvasRef.current
    ) {
      return;
    }

    const rect =
      containerRef.current.getBoundingClientRect();

    const width = Math.floor(rect.width);
    const height = Math.floor(rect.height);

    const ctx =
      canvasRef.current.getContext("2d");

    if (!ctx) {
      return;
    }

    // =====================================================
    // CONFIGURAÇÃO DO CANVAS
    // =====================================================

    canvasRef.current.width = width;
    canvasRef.current.height = height;

    // =====================================================
    // CORES
    // =====================================================

    const colorsArray =
      finalColors.split(",");

    // =====================================================
    // CONTROLE DE PERFORMANCE
    // =====================================================

    const requestedGap =
      parseInt(finalGap, 10);

    /*
      Quantidade máxima de pixels que
      permitiremos criar por card.
    */

    const MAX_PIXELS = 15000;

    /*
      Calculamos aproximadamente quantos
      pixels seriam criados utilizando
      o gap solicitado.
    */

    const estimatedPixels =
      (width / requestedGap) *
      (height / requestedGap);

    /*
      Se ultrapassar o limite,
      aumentamos automaticamente o gap.
    */

    let effectiveGap =
      requestedGap;

    if (
      estimatedPixels >
      MAX_PIXELS
    ) {
      effectiveGap = Math.ceil(
        Math.sqrt(
          (width * height) /
            MAX_PIXELS
        )
      );
    }

    // =====================================================
    // LOG PARA DEBUG
    // =====================================================

    console.log(
      "PixelCard:",
      {
        width,
        height,
        requestedGap,
        effectiveGap,
        estimatedPixels: Math.round(
          estimatedPixels
        ),
        maxPixels: MAX_PIXELS,
      }
    );

    // =====================================================
    // CRIAR PIXELS
    // =====================================================

    const pxs = [];

    for (
      let x = 0;
      x < width;
      x += effectiveGap
    ) {
      for (
        let y = 0;
        y < height;
        y += effectiveGap
      ) {
        const color =
          colorsArray[
            Math.floor(
              Math.random() *
                colorsArray.length
            )
          ];

        const dx =
          x - width / 2;

        const dy =
          y - height / 2;

        const distance =
          Math.sqrt(
            dx * dx +
              dy * dy
          );

        const delay =
          reducedMotion
            ? 0
            : distance;

        pxs.push(
          new Pixel(
            canvasRef.current,
            ctx,
            x,
            y,
            color,
            getEffectiveSpeed(
              finalSpeed,
              reducedMotion
            ),
            delay
          )
        );
      }
    }

    pixelsRef.current = pxs;
  };

  // =========================================================
  // ANIMAÇÃO
  // =========================================================

  const doAnimate = (fnName) => {
    animationRef.current =
      requestAnimationFrame(
        () => doAnimate(fnName)
      );

    const timeNow =
      performance.now();

    const timePassed =
      timeNow -
      timePreviousRef.current;

    const timeInterval =
      1000 / 60;

    if (
      timePassed <
      timeInterval
    ) {
      return;
    }

    timePreviousRef.current =
      timeNow -
      (timePassed %
        timeInterval);

    const ctx =
      canvasRef.current?.getContext(
        "2d"
      );

    if (
      !ctx ||
      !canvasRef.current
    ) {
      return;
    }

    ctx.clearRect(
      0,
      0,
      canvasRef.current.width,
      canvasRef.current.height
    );

    let allIdle = true;

    for (
      let i = 0;
      i < pixelsRef.current.length;
      i++
    ) {
      const pixel =
        pixelsRef.current[i];

      pixel[fnName]();

      if (!pixel.isIdle) {
        allIdle = false;
      }
    }

    if (allIdle) {
      cancelAnimationFrame(
        animationRef.current
      );
    }
  };

  // =========================================================
  // CONTROLAR ANIMAÇÃO
  // =========================================================

  const handleAnimation = (
    name
  ) => {
    cancelAnimationFrame(
      animationRef.current
    );

    animationRef.current =
      requestAnimationFrame(
        () => doAnimate(name)
      );
  };

  const onMouseEnter = () =>
    handleAnimation("appear");

  const onMouseLeave = () =>
    handleAnimation("disappear");

  const onFocus = (e) => {
    if (
      e.currentTarget.contains(
        e.relatedTarget
      )
    ) {
      return;
    }

    handleAnimation("appear");
  };

  const onBlur = (e) => {
    if (
      e.currentTarget.contains(
        e.relatedTarget
      )
    ) {
      return;
    }

    handleAnimation("disappear");
  };

  // =========================================================
  // EFFECT
  // =========================================================

  useEffect(() => {
    initPixels();

    const observer =
      new ResizeObserver(() => {
        initPixels();
      });

    if (containerRef.current) {
      observer.observe(
        containerRef.current
      );
    }

    return () => {
      observer.disconnect();

      cancelAnimationFrame(
        animationRef.current
      );
    };

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    finalGap,
    finalSpeed,
    finalColors,
    finalNoFocus,
  ]);

  // =========================================================
  // RENDER
  // =========================================================

  return (
    <div
      ref={containerRef}
      className={`pixel-card ${className}`}
      onMouseEnter={
        onMouseEnter
      }
      onMouseLeave={
        onMouseLeave
      }
      onFocus={
        finalNoFocus
          ? undefined
          : onFocus
      }
      onBlur={
        finalNoFocus
          ? undefined
          : onBlur
      }
      tabIndex={
        finalNoFocus
          ? -1
          : 0
      }
    >
      <canvas
        className="pixel-canvas"
        ref={canvasRef}
      />

      {children}
    </div>
  );
}