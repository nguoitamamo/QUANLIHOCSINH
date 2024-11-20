const wrapper = document.querySelector(".wrapper");
const slide_card = document.querySelector(".slide-card");
const firstCardWidth = slide_card.querySelector(".card").offsetWidth;
const arrowBtns = document.querySelectorAll(".wrapper i");
const slide_cardChildrens = [...slide_card.children];

let isDragging = false, isAutoPlay = true, startX, startScrollLeft, timeoutId;

// Lấy số lượng thẻ có thể vừa với băng chuyền cùng một lúc
let cardPerView = Math.round(slide_card.offsetWidth / firstCardWidth);

// Chèn bản sao của vài thẻ cuối cùng vào đầu băng chuyền để cuộn vô hạn
slide_cardChildrens.slice(-cardPerView).reverse().forEach(card => {
    slide_card.insertAdjacentHTML("afterbegin", card.outerHTML);
});

// Chèn bản sao của một số thẻ đầu tiên vào cuối băng chuyền để cuộn vô hạn
slide_cardChildrens.slice(0, cardPerView).forEach(card => {
    slide_card.insertAdjacentHTML("beforeend", card.outerHTML);
});

// Cuộn băng chuyền ở vị trí thích hợp để ẩn vài thẻ trùng lặp đầu tiên trên Firefox
slide_card.classList.add("no-transition");
slide_card.scrollLeft = slide_card.offsetWidth;
slide_card.classList.remove("no-transition");

// Thêm trình xử lý sự kiện cho các nút mũi tên để cuộn băng chuyền sang trái và phải
arrowBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        slide_card.scrollLeft += btn.id === "left" ? -firstCardWidth : firstCardWidth;
    });
});

const dragStart = (e) => {
    isDragging = true;
    slide_card.classList.add("dragging");
    // Ghi lại con trỏ ban đầu và vị trí cuộn của băng chuyền
    startX = e.pageX;
    startScrollLeft = slide_card.scrollLeft;
}

const dragging = (e) => {
    if(!isDragging) return; // nếu isDragging là sai trả về từ đây
    // Cập nhật vị trí cuộn của băng chuyền dựa trên chuyển động của con trỏ
    slide_card.scrollLeft = startScrollLeft - (e.pageX - startX);
}

const dragStop = () => {
    isDragging = false;
    slide_card.classList.remove("dragging");
}

const infiniteScroll = () => {
    // Nếu băng chuyền ở đầu, cuộn đến cuối
    if(slide_card.scrollLeft === 0) {
        slide_card.classList.add("no-transition");
        slide_card.scrollLeft = slide_card.scrollWidth - (2 * slide_card.offsetWidth);
        slide_card.classList.remove("no-transition");
    }
    // Nếu băng chuyền ở cuối, cuộn về đầu
    else if(Math.ceil(slide_card.scrollLeft) === slide_card.scrollWidth - slide_card.offsetWidth) {
        slide_card.classList.add("no-transition");
        slide_card.scrollLeft = slide_card.offsetWidth;
        slide_card.classList.remove("no-transition");
    }

    // Xóa thời gian chờ hiện tại và bắt đầu tự động phát nếu chuột không di chuột qua băng chuyền
    clearTimeout(timeoutId);
    if(!wrapper.matches(":hover")) autoPlay();
}

const autoPlay = () => {
    // Tự động phát băng chuyền sau mỗi 2500 ms
    timeoutId = setTimeout(() => slide_card.scrollLeft += firstCardWidth, 2500);
}
autoPlay();

slide_card.addEventListener("mousedown", dragStart);
slide_card.addEventListener("mousemove", dragging);
document.addEventListener("mouseup", dragStop);
slide_card.addEventListener("scroll", infiniteScroll);
wrapper.addEventListener("mouseenter", () => clearTimeout(timeoutId));
wrapper.addEventListener("mouseleave", autoPlay);