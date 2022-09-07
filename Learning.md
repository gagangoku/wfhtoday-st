## How to make a &lt;div&gt; tag clickable and good looking

```css
.wfhBtn {
    font-size: 1rem;
    padding: 10px 30px;
    color: white;
    background: purple;
    border-color: purple;
    border-radius: 8px;
    box-shadow: none;
    cursor: pointer;
    outline: none;
    transition: 0.2s all;
    width: fit-content;
}
.wfhBtn:active {
    transform: scale(0.95);
    box-shadow: 3px 2px 22px 1px rgba(0, 0, 0, 0.24);
    background: purple;
    border-color: purple;
}
.wfhBtn:hover {
    background: black;
    border-color: black;
}
```

Simple and neat !
