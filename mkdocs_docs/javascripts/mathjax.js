window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"], ["$", "$"]],
    displayMath: [["\\[", "\\]"], ["$$", "$$"]],
    processEscapes: true,
    processEnvironments: true,
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex",
  },
};

document$.subscribe(() => {
  const body = document.querySelector(".md-typeset");
  if (body && window.MathJax?.typesetPromise) {
    MathJax.typesetPromise([body]).catch((err) => console.warn("MathJax:", err));
  }
});
