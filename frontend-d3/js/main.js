const width = document.body.clientWidth;
const height = document.body.clientHeight;

const unit = (width-54) / 663;
const wWhite = unit*13, wBlack = unit*9;
const hWhite = unit*66, hBlack = unit*42;
const wLeft = (offset) => offset*(wWhite+1)+1;
const bLeft = (offset) => offset*(wWhite+1)+1-wBlack/2;

const GForce = 60;

const hitColorW = 'rgba(173, 60, 138, 0.65)';
const hitColorB = 'rgba(173, 60, 138, 1)';

const allCats = ['blue', 'green', 'orange', 'pink', 'red', 'sky'];
const getCat = () => {
    const catCol = allCats[Math.floor(Math.random() * allCats.length)];
    return `assets/${catCol}.png`;
}

function initPage() {
    const svg = d3.select('#root').select('svg')
        .attr('width', width)
        .attr('height', height);
    
    const kbgroup = svg.select('#keyboard')
        .style('transform', `translateY(70%)`);
    
    const whites = keyboard_layout.filter(d => d.white);
    const blacks = keyboard_layout.filter(d => !d.white);
    
    const keyboard_white_enter = kbgroup.select('#white')
        .selectAll('rect')
        .data(whites)
        .enter();

    const keyboard_white = keyboard_white_enter.append('rect')
        .attr('height', hWhite)
        .attr('width', wWhite)
        .attr('fill', 'white')
        .attr('_fill', 'white')
        .attr('x', d => wLeft(d.offset))
        .attr('stroke', 'gray')
        .attr('stroke-width', '1px');
    
    const keyboard_text = keyboard_white_enter.append('text')
        .attr('text-anchor', 'middle')
        .attr('x', d => wLeft(d.offset) + wWhite/2)
        .attr('y', hWhite*0.85)
        .attr('pointer-events', 'none')
        .attr('font-size', '0.8rem')
        .text(d => d.name);
    
    const keyboard_black = kbgroup.select('#black')
        .selectAll('rect')
        .data(blacks)
        .enter()
        .append('rect')
        .attr('height', hBlack)
        .attr('width', wBlack)
        .attr('fill', 'black')
        .attr('_fill', 'black')
        .attr('x', d => bLeft(d.offset))
        .attr('stroke', 'gray')
        .attr('stroke-width', '1px');
}

function drawAnimation(midijson) {
    console.log(midijson.length);

    const svg = d3.select('#root').select('svg');
    const whites = svg.select('#white').selectAll('rect');
    const blacks = svg.select('#black').selectAll('rect');
    const cats = svg.select('#cat');

    midijson.forEach(ele => {
        const keyid = ele.midi_note - 21;

        let keyR = whites.filter(d => d.index == keyid);
        let isWhite = true;
        if (keyR.nodes().length === 0) {
            keyR = blacks.filter(d => d.index == keyid);
            isWhite = false;
        }

        const hitColor = isWhite? hitColorW: hitColorB;
        const catSize = isWhite? wWhite: wBlack;

        const catFile = getCat();
        const newCat = cats.append('image')
            .attr('width', catSize)
            .attr('height', catSize)
            .attr('xlink:href', catFile)
            .attr('x', keyR.attr('x'))
            .attr('y', 0)
            .attr('opacity', 0);

        const intensity = ele.velocity;
        newCat.speed = -(intensity/128*140+120);
        const updateGap = 10;

        setTimeout(function() {
            keyR.attr('fill', hitColor);

            newCat.attr('opacity', 1);

            const catTimer = setInterval(function() {
                const nowY = parseFloat(newCat.attr('y'));

                if (nowY > 0.3*height) {
                    newCat.remove();
                    clearInterval(catTimer);
                }
                else if (nowY > 0) {
                    newCat.attr('opacity', 0);
                }

                const nextSpeed = newCat.speed + GForce*updateGap/1000;
                const nextY = nowY + (newCat.speed + nextSpeed)/2 * updateGap / 1000;
                newCat.attr('y', nextY);
                newCat.speed = nextSpeed;

            }, updateGap);

        }, ele.onset_time * 1000);

        setTimeout(function() {
            keyR.attr('fill', keyR.attr('_fill'));
        }, ele.offset_time * 1000);
    });
}

initPage();
//d3.json('data/2.4pv.json').then(drawAnimation);