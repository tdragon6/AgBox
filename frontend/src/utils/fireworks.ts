import confetti from 'canvas-confetti';

export const useFireworks = () => {
  const fire = () => {
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 },
      colors: ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff'],
      zIndex: 9999,
    });
  };

  const fireSides = () => {
    const end = Date.now() + 800;

    const frame = () => {
      confetti({
        particleCount: 4,
        angle: 60,
        spread: 55,
        origin: { x: 0, y: 0.7 },
        colors: ['#ff6416', '#fff6b7', '#f6416c'],
      });
      confetti({
        particleCount: 4,
        angle: 120,
        spread: 55,
        origin: { x: 1, y: 0.7 },
        colors: ['#165eff', '#b7f6ff', '#416cf6'],
      });

      if (Date.now() < end) {
        requestAnimationFrame(frame);
      }
    };
    frame();
  };

  const fireRing = () => {
    confetti({
      particleCount: 200,
      spread: 360,
      startVelocity: 30,
      origin: { x: 0.5, y: 0.5 },
      colors: [
        '#26ccff',
        '#a25afd',
        '#ff5e7e',
        '#88ff5a',
        '#fcff42',
        '#ffa62d',
      ],
    });
  };

  return { fire, fireSides, fireRing };
};

export default useFireworks;
