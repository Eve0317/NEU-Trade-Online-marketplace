from django.shortcuts import render, get_object_or_404

from .models import Item

from .models import Category, Item

# Searching Items.
# Defining a Django view function named items that takes an HTTP request as a parameter.
def items(request):

    # Getting the value of the query parameter named query, or an empty string if it doesn't exist.
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)

    # Querying the database for all categories.
    categories = Category.objects.all()  

    # Querying the database for all items that have not been sold.
    items = Item.objects.filter(is_sold=False)

    # Filtering the items to only include items whose category matches the category_id.
    if category_id:
        items = items.filter(category_id=category_id)
    
    # Filtering the items to only include items whose title contains the query.
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Using the render function to generate an HTTP response.
    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        })

# Create your views here.
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold = False).exclude(pk=pk)[0:3]


    return render(request, 'item/detail.html',{
        'item': item,
        "related_items": related_items
    })