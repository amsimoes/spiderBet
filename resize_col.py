POST https://sheets.googleapis.com/v4/spreadsheets/spreadsheetId:batchUpdate

{
  "requests": [
    {
      "autoResizeDimensions": {
        "dimensions": {
          "sheetId": sheetId,
          "dimension": "COLUMNS",
          "startIndex": 0,
          "endIndex": 3
        }
      }
    }
  ]
}
