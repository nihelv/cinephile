function Slider(target) {
  let index = 1;
  let isMoved = true;
  const speed = 1500; // ms

  const transform = "transform " + speed / 1000 + "s";
  let translate = (i) => "translateY(-" + 100 * i + "%)";

  const slider = document.querySelector(target);
  const sliderRects = slider.getClientRects()[0];
  slider.style["overflow"] = "hidden";

  const container = document.createElement("div");
  container.style["display"] = "flex";
  container.style["flex-direction"] = "column";
  container.style["width"] = sliderRects.width + "px";
  container.style["height"] = 24 + "px";
  container.style["transform"] = translate(index);

  let boxes = [].slice.call(slider.children);
  boxes = [].concat(boxes[boxes.length - 1], boxes, boxes[0]);

  const size = boxes.length;
  for (let i = 0; i < size; i++) {
    const box = boxes[i];
    if (i === 11) {
      box.children[0].textContent = 1
    } else {
      box.children[0].textContent = i
    }
    box.style["height"] = "100%";
    box.style["width"] = "100%";
    container.appendChild(box.cloneNode(true));
  }

  container.addEventListener("transitionstart", function () {
    isMoved = false;
    setTimeout(() => {
      isMoved = true;
    }, speed);
  });
  container.addEventListener("transitionend", function () {
    if (index === size - 1) {
      index = 1;
      container.style["transition"] = "none";
      container.style["transform"] = translate(index);
    }
    if (index === 0) {
      index = size - 1;
      container.style["transition"] = "none";
      container.style["transform"] = translate(index);
    }
  });

  slider.innerHTML = "";
  slider.appendChild(container);

  return {
    move: function (i) {
      if (isMoved === true) {
        index = i;
        container.style["transition"] = transform;
        container.style["transform"] = translate(index);
      }
    },
    next: function () {
      if (isMoved === true) {
        index = (index + 1) % size;
        container.style["transition"] = transform;
        container.style["transform"] = translate(index);
      }
    },
    prev: function () {
      if (isMoved === true) {
        index = index === 0 ? index + size : index;
        index = (index - 1) % size;
        container.style["transition"] = transform;
        container.style["transform"] = translate(index);
      }
    }
  };
}

const s1 = new Slider("#slider");

setInterval(() => {
  s1.next();
}, 1500)