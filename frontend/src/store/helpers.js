/* If these functions become fragile replace with `normalizr` package */

export function normalizeRelations(data, fields) {
  return {
    ...data,
    ...fields.reduce((prev, field) => {
      if (!data[field]) return null;
      return {
        ...prev,
        [field]: Array.isArray(data[field])
          ? data[field].map((x) => x.id)
          : data[field].id,
      };
    }, {}),
  };
}

export function resolveRelations(data, fields, rootGetters) {
  if (!data) return data;
  let key, relation;
  const resolvedFields = fields.reduce((prev, field) => {
    if (Array.isArray(field)) {
      key = field[0];
      relation = field[1];
    } else {
      key = field;
      relation = field;
    }
    return {
      ...prev,
      [key]: Array.isArray(data[key])
        ? data[key].map((x) => rootGetters[`${relation}/find`](x))
        : rootGetters[`${relation}/find`](data[key]),
    }
  }, {});
  
  return {
    ...data,
    ...resolvedFields,
  };
}
