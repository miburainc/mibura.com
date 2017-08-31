export default {
    getStripe: state => state.stripe,
    getMultiplier: state => name => {
      for (let i=0; i<state.multiplier.length; i++) {
        let cat = state.multiplier[i]
        if (cat.category_code == name) {
          return cat
        }
      }
    },
    getBrands: state => state.brands,
    getDiscounts: state => state.discounts,
    getCurrentDiscount: (state, store) => {
      let years = store.getSupportMonths/12
      let discount = 0.0
      
      for (let i=0; i<state.discounts.length; i++) {
        if (state.discounts[i].year_threshold <= years) {
          if (discount < state.discounts[i].discount_percent) {
            discount = state.discounts[i].discount_percent
          }
        }
      }
      return discount
    },
    getAPIRoot: state => state.api_root,
    getErrors: state => state.errors,
    
    getPurchaseSuccess: state => state.purchase_success,
    getAcceptedTerms: state => state.accepted_terms,
    getPaymentToken: state => {
      if (state.stripe.ach_payment_token) {
        return state.stripe.ach_payment_token
      }
      else if (state.stripe.cc_payment_token) {
        return state.stripe.cc_payment_token
      }
      else {
        return ""
      }
    },
  }