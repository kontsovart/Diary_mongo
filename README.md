###API 
Массив графиков 

````
charts: [
	{   id: 1,
		"title": "График посещаемости занятий по физкультуре",
		"type": "line", #pie
		"oxName": "Дата",
		"oyName": "Кол-во посещений, дн.",
		"series": [
			{
                id: 1,
				"lineTitle": "8 А класс",
				data = [{
				  "date": "2015-01-01",
				  "value": 23
				}, {
				  "date": "2015-01-01",
				  "value": 23
				}, {
				  "date": "2015-01-01",
				  "value": 12
				}, {
				  "date": "2015-01-01",
				  "value": 30
				}]
			},
			{
                id: 2,
				"lineTitle": "8 Б класс",
				data = [{
				  "date": "2015-02-01",
				  "value": 11
				}, {
				  "date": "2015-02-01",
				  "value": 15
				}, {
				  "date": "2015-01-02",
				  "value": 17
				}, {
				  "date": "2015-02-01",
				  "value": 18
				}]
			}
		] 	
	}
]
````

tree view 

````
treeview = {
    id: 1,
    name: 'root',
    toggled: true,
    children: [
        {
            id: 2,
            name: 'parent',
            children: [
                { name: 'child1', id: 3 },
                { name: 'child2', id: 4 }
            ]
        },
        {
            id: 5,
            name: 'parent',
            children: []
        },
        {
            id: 6,
            name: 'parent',
            children: [
                {
                    id: 7,
                    name: 'nested parent',
                    children: [
                        { id: 8, name: 'nested child 1' },
                        { id: 9, name: 'nested child 2' }
                    ]
                }
            ]
        }
    ]
}
````