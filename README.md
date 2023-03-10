# Musa

An intelligent wealth-aggregator.

## TODO

```
[ ] Clean up trading holidays
[ ] 
```

## Data Sources

### Precompiled

- https://stooq.com/db/h/

## Changelog

```
2023-03-03
- Modified Stock to interface with the historical database vs. having Market do it
- Created DatabaseHandler to facilitate queries with the SQL database

2023-03-01
- Created Market and Stock classes as well as supporting smaller classes to facilitate their functionality
- Downloaded pre-scraped stock market data for US markets from stooq.com
```