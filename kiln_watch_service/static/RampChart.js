function RampChart(width, height, debug) {
    const DEBUG = debug | false;
    const WIDTH = width;
    const HEIGHT = height;
    const MARGINS = {
        top: 50,
        right: 50,
        bottom: 60,
        left: 80
    };
    const XRANGE = 12;
    const YRANGE = 300;
    const PREFIX = "r_";

    const xScale = d3.scaleLinear()
        .range([MARGINS.left, WIDTH - MARGINS.right])
        .domain([-XRANGE, 0]);
    const yScale = d3.scaleLinear().range([HEIGHT - MARGINS.bottom, MARGINS.top])
        .domain([-YRANGE, YRANGE]);

    this.createChart = function() {

        // The graph image
        var svg = d3.create("svg")
            .attr("width", WIDTH)
            .attr("height", HEIGHT)
            .attr("viewBox", [0, 0, WIDTH, HEIGHT])
            .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

        // Title
        svg.append('text')
            .attr('class', 'chart-title')
            .text("Rate of Change")
            .attr('x', MARGINS.left + (WIDTH - MARGINS.left - MARGINS.right) / 2)
            .attr('y', MARGINS.bottom / 4)
            .attr("text-anchor", "middle");

        // Border around SVG, used for debugging mostly
        if (DEBUG) {
            var borderPath = svg.append("rect")
                .attr("x", 0)
                .attr("y", 0)
                .attr("height", HEIGHT)
                .attr("width", WIDTH)
                .style("stroke", 'red')
                .style("fill", "none")
                .style("stroke-width", 1);
        }

        // Add the x-axis bottom
        var xAxisBottom = (g) => g
            .attr('transform', `translate(0,${HEIGHT - MARGINS.bottom})`)
            .call(d3.axisBottom(xScale));
        svg.append("g").call(xAxisBottom);
        svg.append('text')
            .attr('class', 'axis-label')
            .text("Age (hours)")
            .attr('x', MARGINS.left + (WIDTH - MARGINS.left - MARGINS.right) / 2)
            .attr('y', HEIGHT - MARGINS.bottom / 4)
            .attr("text-anchor", "middle");

        // Add the x-axis top
        var xAxisTop = (g) => g
            .attr('transform', `translate(0,${MARGINS.top})`)
            .call(d3.axisTop(xScale).tickFormat(''));
        svg.append("g").call(xAxisTop);

        // Add the y-axis left
        var yAxisLeft = (g) => g
            .attr('transform', `translate(${MARGINS.left},0)`)
            .call(d3.axisLeft(yScale));
        svg.append("g").call(yAxisLeft);
        svg.append('text')
            .attr('class', 'axis-label')
            .text('Rate of Change')
            .attr('transform', 'rotate(-90)')
            .attr('x', -(MARGINS.top + (HEIGHT - MARGINS.top - MARGINS.bottom) / 2))
            .attr('y', MARGINS.left / 4)
            .attr("text-anchor", "middle");

        // Add the y-axis right
        var yAxisRight = (g) => g
            .attr('transform', `translate(${WIDTH - MARGINS.right}, 0)`)
            .call(d3.axisRight(yScale));
        svg.append("g").call(yAxisRight);

        // Horizontal grid lines
        var hGrid = (g) => g
            .attr('class', 'grid-lines')
            .selectAll('line')
            .data(xScale.ticks())
            .join('line')
            .attr('x1', d => xScale(d))
            .attr('x2', d => xScale(d))
            .attr('y1', MARGINS.top)
            .attr('y2', HEIGHT - MARGINS.bottom)
            .style("stroke", "grey")
            .style("stroke-opacity", "0.2");
        svg.append('g').call(hGrid);

        // Vertical grid lines
        var vGrid = (g) => g
            .attr('class', 'grid-lines')
            .selectAll('line')
            .data(yScale.ticks())
            .join('line')
            .attr('x1', MARGINS.left)
            .attr('x2', WIDTH - MARGINS.right)
            .attr('y1', d => yScale(d))
            .attr('y2', d => yScale(d))
            .style("stroke", "grey")
            .style("stroke-opacity", "0.2");
        svg.append('g').call(vGrid);

        // Last Updated text
        svg.append('text')
            .attr('class', 'axis-label')
            .attr('id', `${PREFIX}last_updated`)
            .text("")
            .attr('x', WIDTH - MARGINS.right)
            .attr('y', HEIGHT - MARGINS.bottom / 4)
            .attr("text-anchor", "end");

        return svg;
    }

    this.updateChartData = function(svg, data) {

        // Order data by index
        data.sort((a, b) => a.index - b.index);

        // Remove any existing lines
        data.forEach(function(sensor) {
            d3.select(`#${PREFIX}${sensor.name}`).remove();
        });

        // Declare the line generator.
        const line = d3.line()
            .x(d => xScale(d.time_late))
            .y(d => yScale(d.rate));

        // Draw the lines.
        data.forEach(function(sensor) {
            svg.append('path')
                .datum(sensor.ramps)
                .attr('id', `${PREFIX}${sensor.name}`)
                .attr('d', line)
                .style('fill', 'none')
                .style('stroke', STROKE[sensor.index % STROKE.length])
                .style('stroke-dasharray', DASH[sensor.index % DASH.length]);
        });

        // update the timestamp
        var now = new Date();
        d3.select(`#${PREFIX}last_updated`).text("Updated: "
                    + (now.getMonth()+1)  + "/"
                    + now.getDate() + "/"
                    + now.getFullYear() + " @ "
                    + (now.getHours() < 10 ? '0' : '') + now.getHours() + ":"
                    + (now.getMinutes() < 10 ? '0' : '') + now.getMinutes());

    }

}