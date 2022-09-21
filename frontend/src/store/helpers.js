/* 
  Sept 2022 refactor has made some of these unnecessary.
  TODO
  Or we can refactor slightly; but with better efficiency than before
    by return related objects again but now loaded with our new cached `loadOne` actions.
*/

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

export function renameRelation(data, fields) {
  const renameFields = fields.reduce((prev, fieldRename) => {
    const value = data[fieldRename[0]];
    delete data[fieldRename[0]];
    return {
      ...prev,
      [fieldRename[1]]: value,
    };
  }, {});
  return {
    ...data,
    ...renameFields,
  };
}

export function loadRelations(data, fields, rootGetters) {
  Object.entries(fields).forEach(([key, relation]) => {
    rootGetters[`${relation}/loadOne`](data[key])
  });
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
