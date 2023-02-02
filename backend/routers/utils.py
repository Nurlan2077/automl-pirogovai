def compare_items(old_item, new_item):
    updates = []
    for old_pair, new_pair in zip(old_item, new_item):
        if old_pair[1] != new_pair[1]:
            updates.append((new_pair[0], new_pair[1]))
    return updates


def make_where_id_condition(id_names: list):
    condition = " where "
    condition_parts = []
    for id_name in id_names:
        condition_parts.append(f"{id_name} = ?")
    return condition + " and ".join(condition_parts)


def append_ids(inserts: list, item_ids: list):
    for item_id in item_ids:
        inserts.append(item_id)


def make_update_statement(item_ids: list, table_name: str, id_names: list, updates: list):
    statement = f"update {table_name} set "
    item_row = []
    inserts = []
    for pair in updates:
        item_row.append(f"{pair[0]} = ?")
        inserts.append(pair[1])
    append_ids(inserts, item_ids)
    where_condition = make_where_id_condition(id_names)
    statement += ", ".join(item_row) + where_condition
    return statement, (*inserts,)
