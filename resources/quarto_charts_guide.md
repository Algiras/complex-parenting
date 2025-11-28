# Adding Data Visualizations to Quarto Books

## Overview
Quarto supports multiple approaches for adding interactive charts and data visualizations to books.

## Option 1: Observable JavaScript (OJS) - RECOMMENDED
**Pros:** Native Quarto support, works without Python/R, interactive, no server needed
**Cons:** Requires learning Observable Plot syntax (similar to ggplot2)

### Basic Example
```{ojs}
//| echo: false
data = [
  {condition: "Bipolar Only", percentage: 15},
  {condition: "ADHD Only", percentage: 25},
  {condition: "Bipolar + ADHD", percentage: 70}
]

Plot.plot({
  marks: [
    Plot.barY(data, {x: "condition", y: "percentage", fill: "steelblue"}),
    Plot.ruleY([0])
  ],
  y: {label: "Percentage (%)", grid: true},
  x: {label: "Condition"},
  marginBottom: 60
})
```

## Option 2: Mermaid Diagrams
**Pros:** Simple syntax, built-in Quarto support
**Cons:** Limited to flowcharts/diagrams, not data charts

### Example
```{mermaid}
graph TD
    A[Stimulant Treatment] --> B{Mood Stable?}
    B -->|No| C[6-7x Mania Risk]
    B -->|Yes| D[Safe to Proceed]
```

## Option 3: Python/Plotly (If Python env available)
**Pros:** Powerful, familiar to data scientists
**Cons:** Requires Python setup

## Recommended Charts for This Book

1. **Chapter 1 (Stats):** Bar chart of comorbidity rates
2. **Chapter 2 (Manic Rage vs Meltdown):** Comparison table (already done)
3. **Chapter 4 (The Blur):** Timeline visualization of cycling patterns
4. **Chapter 5 (Stimulant Trap):** Risk flowchart
5. **Chapter 7 (Sleep):** Circadian rhythm visualization

## Implementation Strategy
Use **Observable JS** for data charts and **Mermaid** for flowcharts.
