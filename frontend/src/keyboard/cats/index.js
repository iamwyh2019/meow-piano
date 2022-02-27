import Blue from './assets/blue.png';
import Green from './assets/green.png';
import Orange from './assets/orange.png';
import Pink from './assets/pink.png';
import Red from './assets/red.png';
import Sky from './assets/sky.png';

const Cat = ({cat_width, left, bottom}) => {
    const colors = [Blue, Green, Orange, Pink, Red, Sky];
    const cat_file = colors[Math.floor(Math.random() * colors.length)];
    const cat_style = {
        width: cat_width + 'px',
        height: cat_width + 'px',
        background: `url(${cat_file}) no-repeat`,
        backgroundSize: `${cat_width}px ${cat_width}px`,
        position: 'absolute',
        left: left,
        bottom: bottom,
    };

    return <div style={cat_style}></div>
}

export default Cat;