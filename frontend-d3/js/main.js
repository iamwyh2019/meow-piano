const width = document.body.clientWidth;
const height = document.body.clientHeight;

const unit = (width-54) / 663;
const wWhite = unit*13, wBlack = unit*9;
const hWhite = unit*66, hBlack = unit*42;
const wLeft = (offset) => offset*(wWhite+1)+1;
const bLeft = (offset) => offset*(wWhite+1)+1-wBlack/2;

const hitColorW = 'rgba(173, 60, 138, 0.65)';
const hitColorB = 'rgba(173, 60, 138, 1)';

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
    const svg = d3.select('#root').select('svg');
    const whites = svg.select('#white').selectAll('rect');
    const blacks = svg.select('#black').selectAll('rect');

    midijson.forEach(ele => {
        const keyid = ele.midi_note - 21;

        // Try find it
        let keyR = whites.filter(d => d.index == keyid);
        let hitColor = hitColorW;
        if (keyR.nodes().length === 0) {
            keyR = blacks.filter(d => d.index == keyid);
            hitColor = hitColorB;
        }

        setTimeout(function() {
            keyR.attr('fill', hitColor);
        }, ele.onset_time * 1000);

        setTimeout(function() {
            keyR.attr('fill', keyR.attr('_fill'));
        }, ele.offset_time * 1000);
    });
}

initPage();
d3.json('data/snowflake.json').then(drawAnimation);