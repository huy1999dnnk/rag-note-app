import { useState, useCallback } from 'react';

export function useElementSize<T extends HTMLElement>() {
  const [size, setSize] = useState({ width: 0, height: 0 });
  const ref = useCallback((node: T | null) => {
    if (!node) return;

    const updateSize = () => {
      setSize({
        width: node.offsetWidth,
        height: node.offsetHeight,
      });
    };

    updateSize(); // Initial size

    const observer = new ResizeObserver(() => updateSize());
    observer.observe(node);

    return () => observer.disconnect();
  }, []);

  return { ref, ...size };
}
